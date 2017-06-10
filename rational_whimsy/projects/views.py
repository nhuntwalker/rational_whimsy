"""Views for the projects app."""
from django.db.models import Count
from django.views.generic import ListView, DetailView
from projects.models import Project
# from django.views.generic.edit import CreateView, UpdateView, DeleteView


class ListProjects(ListView):
    """List all of the individual projects."""

    model = Project
    template_name = "project/project_list.html"
    queryset = Project.published.all()
    paginate_by = 5

    def get_context_data(self, **kwargs):
        """Adding a bit more to the context."""
        context = super(ListProjects, self).get_context_data(**kwargs)
        context["page"] = "projects"
        context["tag_list"] = Project.tags.values(
            'name'
        ).annotate(
            count=Count('name')
        ).order_by('-count')[:100]
        return context


class ListTaggedProjects(ListView):
    """List all of the projects matching a tag."""

    model = Project
    template_name = "project/project_list.html"
    queryset = Project.published.all()
    paginate_by = 5

    def get_context_data(self, **kwargs):
        """Need to add a bit more context."""
        context = super(ListTaggedProjects, self).get_context_data(**kwargs)
        context["page"] = "projects"
        context["tag_list"] = Project.tags.values(
            'name'
        ).annotate(
            count=Count('name')
        ).order_by('-count')[:100]
        context['main_tag'] = self.kwargs['tag']
        return context

    def get_queryset(self):
        """Only select particular projects that have the given tag."""
        queryset = super(ListTaggedProjects, self).get_queryset()
        queryset = queryset.filter(tags__name__in=[self.kwargs['tag']])
        return queryset


class ProjectDetail(DetailView):
    """Show the detail for an individual project."""

    model = Project
    template_name = "project/project_detail.html"
    query_pk_and_slug = True
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        """Just add the page name to the context."""
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        context['page'] = 'project'
        return context
