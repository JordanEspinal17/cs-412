from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.shortcuts import render
from datetime import datetime
import plotly
import plotly.graph_objs as go
from plotly.offline import plot
from .models import Voter
from django.db.models import Count

class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voters.html'
    context_object_name = 'voters'
    paginate_by = 50

    def get_queryset(self):
        qs = super().get_queryset()
        city = self.request.GET.get('city', None)
        if city:
            qs = qs.filter(street_name__icontains=city)
        return qs
class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voters.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add election fields list to the context
        context['election_fields'] = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        # Add other context data like filters
        context['party_affiliations'] = Voter.objects.values_list('party_affiliation', flat=True).distinct()
        context['years'] = range(1900, datetime.now().year + 1)
        context['voter_scores'] = range(6)  # Assuming voter_score ranges from 0 to 5
        return context

class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add Google Maps URL
        voter = context['voter']
        address = f"{voter.street_number} {voter.street_name}, {voter.zip_code}".replace(' ', '+')
        context['google_maps_url'] = f"https://www.google.com/maps?q={address}"
        return context
    
class VoterGraphsView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()

        # Add election fields to the context
        context['election_fields'] = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']

        # Graph 1: Distribution of Voters by Year of Birth
        years_of_birth = qs.values_list('date_of_birth', flat=True)
        year_counts = {}
        for dob in years_of_birth:
            year = dob.year
            year_counts[year] = year_counts.get(year, 0) + 1
        graph1 = go.Bar(x=list(year_counts.keys()), y=list(year_counts.values()))
        context['graph1'] = plot({"data": [graph1],
                                  "layout": go.Layout(title="Voters by Year of Birth")},
                                 auto_open=False, output_type="div")

        # Graph 2: Distribution of Voters by Party Affiliation
        party_counts = qs.values('party_affiliation').annotate(count=Count('party_affiliation'))
        labels = [item['party_affiliation'] for item in party_counts]
        values = [item['count'] for item in party_counts]
        graph2 = go.Pie(labels=labels, values=values)
        context['graph2'] = plot({"data": [graph2],
                                  "layout": go.Layout(title="Voters by Party Affiliation")},
                                 auto_open=False, output_type="div")

        # Graph 3: Distribution of Voters by Election Participation
        election_counts = {field: qs.filter(**{field: True}).count() for field in context['election_fields']}
        graph3 = go.Bar(x=list(election_counts.keys()), y=list(election_counts.values()))
        context['graph3'] = plot({"data": [graph3],
                                  "layout": go.Layout(title="Voters by Election Participation")},
                                 auto_open=False, output_type="div")

        # Add other filter data
        context['party_affiliations'] = Voter.objects.values_list('party_affiliation', flat=True).distinct()
        context['years'] = range(1900, datetime.now().year + 1)
        context['voter_scores'] = range(6)  # Assuming voter_score ranges from 0 to 5
        return context
