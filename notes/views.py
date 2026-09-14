import re
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from .models import Note, Category, NoteAttachment


def extract_search_context(text, query, context_words=10):
    """
    Extracts snippets of text surrounding the search query.
    Returns a list of dictionaries containing the snippet and a highlighted version.
    """
    if not query or not text:
        return []
    
    # Split into sentences (simple split by punctuation)
    sentences = re.split(r'(?<=[.!?]) +', text)
    matches = []
    
    # Escape query for regex and compile case-insensitive pattern
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    
    for sentence in sentences:
        if pattern.search(sentence):
            # Highlight the match in the sentence
            highlighted = pattern.sub(
                lambda match: f'<mark class="bg-amber-200 text-amber-900 font-bold px-0.5 rounded">{match.group(0)}</mark>',
                sentence
            )
            matches.append({
                'raw': sentence,
                'highlighted': mark_safe(highlighted)
            })
            
    return matches

def note_list(request):
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '')
    
    notes = Note.objects.all().order_by('-service_date')
    
    # Structured list for search results if a query exists
    search_results = []

    if query:
        notes = notes.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
        
        # Build context snippets for each matching note
        for note in notes:
            # Check title first
            title_match = bool(re.search(re.escape(query), note.title, re.IGNORECASE))
            
            # Extract snippets from content
            content_snippets = extract_search_context(note.content, query)
            
            search_results.append({
                'note': note,
                'title_match': title_match,
                'snippets': content_snippets
            })

    if category_id:
        if category_id == 'none':
            notes = notes.filter(category__isnull=True)
            # Filter search results if category also applied
            if query:
                 search_results = [res for res in search_results if res['note'].category is None]
        else:
            notes = notes.filter(category_id=category_id)
            if query:
                 search_results = [res for res in search_results if res['note'].category_id == int(category_id)]

    categories = Category.objects.all()
    
    return render(request, 'notes/note_list.html', {
        'notes': notes,
        'categories': categories,
        'query': query,
        'search_results': search_results,
        'selected_category': category_id,
    })

def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'notes/note_detail.html', {'note': note})

def note_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')
        service_date = request.POST.get('service_date')
        
        category = Category.objects.filter(id=category_id).first() if category_id else None
        
        note = Note.objects.create(
            title=title, 
            content=content, 
            category=category,
            service_date=service_date
        )

        # Handle file uploads + captions
        files = request.FILES.getlist('attachments')
        captions = request.POST.getlist('captions')

        for f, caption in zip(files, captions):
            NoteAttachment.objects.create(
                note=note, 
                file=f, 
                caption=caption.strip() if caption else None
            )

        return redirect('note_detail', pk=note.pk)

    categories = Category.objects.all()
    return render(request, 'notes/note_form.html', {'categories': categories})


def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk)
    
    if request.method == 'POST':
        note.title = request.POST.get('title')
        note.content = request.POST.get('content')
        category_id = request.POST.get('category')
        note.service_date = request.POST.get('service_date')
        
        note.category = Category.objects.filter(id=category_id).first() if category_id else None
        note.save()

        # 1. Update captions for existing attachments
        for attachment in note.attachments.all():
            existing_caption = request.POST.get(f'existing_caption_{attachment.id}')
            if existing_caption is not None:
                attachment.caption = existing_caption.strip()
                attachment.save()

        # 2. Delete selected existing attachments
        delete_attachment_ids = request.POST.getlist('delete_attachments')
        if delete_attachment_ids:
            attachments_to_delete = note.attachments.filter(id__in=delete_attachment_ids)
            for attachment in attachments_to_delete:
                attachment.file.delete(save=False)
            attachments_to_delete.delete()

        # 3. Save new uploaded attachments + captions
        files = request.FILES.getlist('attachments')
        captions = request.POST.getlist('captions')

        for f, caption in zip(files, captions):
            NoteAttachment.objects.create(
                note=note, 
                file=f, 
                caption=caption.strip() if caption else None
            )

        return redirect('note_detail', pk=note.pk)

    categories = Category.objects.all()
    return render(request, 'notes/note_form.html', {
        'note': note, 
        'categories': categories
    })

def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')
    return render(request, 'notes/note_confirm_delete.html', {'note': note})


# --- Category CRUD Views ---
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'notes/category_list.html', {'categories': categories})

def category_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        color = request.POST.get('color', '#3B82F6')
        slug = slugify(name)
        
        Category.objects.create(name=name, slug=slug, color=color)
        return redirect(request.META.get('HTTP_REFERER', 'note_list'))

def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.color = request.POST.get('color', '#3B82F6')
        category.slug = slugify(category.name)
        category.save()
        return redirect('category_list')
        
    return render(request, 'notes/category_form.html', {'category': category})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'notes/category_confirm_delete.html', {'category': category})