from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import generate_nonogram_grid, get_row_clues, get_column_clues, get_reverse_column_clues

# Create your views here.


class CreateGameView(LoginRequiredMixin, View):
    template_name = 'game/create_game.html'

    def get(self, request):
        grid = generate_nonogram_grid(20, 20)
        row_clues, max_row_clues = get_row_clues(grid)
        column_clues, max_column_clues = get_column_clues(grid)
        context = {
            'grid': grid,
            'row_clues': row_clues,
            'column_clues': column_clues,
            'rows': len(grid),
            'columns': len(grid[0]),
            'max_row_clues': max_row_clues,
            'max_column_clues': max_column_clues
        }
        return render(request, self.template_name, context)
