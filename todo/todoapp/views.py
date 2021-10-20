from django.shortcuts import render,redirect
from django.urls import reverse_lazy

from .models import todo
from .form import todoform
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView,DeleteView



class Tasklistview(ListView):
    model = todo
    template_name = 'home.html'
    context_object_name = 'task'
class detailview(DetailView):
    model = todo
    template_name = 'detail.html'
    context_object_name = 'i'

class updateview(UpdateView):
    model = todo
    template_name = 'update.html'
    context_object_name = 'i'
    fields = ('task','priority','date')

    def get_success_url(self):
        return reverse_lazy('detail',kwargs={'pk':self.object.id})

class deleteview(DeleteView):
    model = todo
    template_name = 'delete.html'
    success_url = reverse_lazy('cbvhome')


# Create your views here.
def home(request):
    if request.method == "POST":
        task=request.POST.get('task','')
        priority=request.POST.get('priority','')
        date = request.POST.get('date','')
        obj= todo(task=task,priority=priority,date=date)
        obj.save()
        return redirect('/')

    obj = todo.objects.all()
    return render(request,'home.html',{'task':obj})
def delete(request,id):
    obj = todo.objects.get(id=id)
    if request.method =='POST':
        obj.delete()
        return redirect('/')
    return render(request, 'delete.html')
def update(request,id):
    obj = todo.objects.get(id=id)
    f = todoform(request.POST or None, instance=obj)
    if f.is_valid():
        f.save()
        return redirect('/')
    return render(request,'edit.html',{'f':f,'task':obj})
