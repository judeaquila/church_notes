# notes/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.utils.text import slugify
from .models import Note, Category, NoteAttachment

# --- Note Views ---
def note_list(request):
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '')
    
    notes = Note.objects.all().order_by('-updated_at')

    if query:
        notes = notes.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    if category_id:
        if category_id == 'none':
            notes = notes.filter(category__isnull=True)
        else:
            notes = notes.filter(category_id=category_id)

    categories = Category.objects.all()
    
    return render(request, 'notes/note_list.html', {
        'notes': notes,
        'categories': categories,
        'query': query,
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
        
        category = Category.objects.get(id=category_id) if category_id else None
        note = Note.objects.create(title=title, content=content, category=category)

        files = request.FILES.getlist('attachments')
        for f in files:
            NoteAttachment.objects.create(note=note, file=f)

        return redirect('note_detail', pk=note.pk)

    categories = Category.objects.all()
    return render(request, 'notes/note_form.html', {'categories': categories})

def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.title = request.POST.get('title')
        note.content = request.POST.get('content')
        category_id = request.POST.get('category')
        note.category = Category.objects.get(id=category_id) if category_id else None
        note.save()

        files = request.FILES.getlist('attachments')
        for f in files:
            NoteAttachment.objects.create(note=note, file=f)

        return redirect('note_detail', pk=note.pk)

    categories = Category.objects.all()
    return render(request, 'notes/note_form.html', {'note': note, 'categories': categories})

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