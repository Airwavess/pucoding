from django.contrib import admin
from .models import Student, LearningClub, Score

class StudentAdmin(admin.ModelAdmin):
	list_display = ('st_id', 'st_name', 'st_class', 'lc_id')

class LearningClubAdmin(admin.ModelAdmin):
	list_display = ('lc_id', 'lc_name', 'lc_TA', 'lc_teacher')
		
class ScoreAdmin(admin.ModelAdmin):
	list_display = ('st_id', 'sc_week', 'sc_num_of_cpl', 'sc_level')

admin.site.register(Student, StudentAdmin)
admin.site.register(Score, ScoreAdmin)
admin.site.register(LearningClub, LearningClubAdmin)
