from django.db import models

class Student(models.Model):
	st_id = models.TextField(primary_key = True)
	st_name = models.TextField()
	st_class = models.TextField()
	lc_id = models.ForeignKey('LearningClub')
	

class LearningClub(models.Model):
	lc_id = models.AutoField(primary_key = True)
	lc_name = models.TextField()
	lc_TA = models.TextField()
	lc_teacher = models.CharField(max_length = 5)

class Score(models.Model):
	st_id = models.ForeignKey('Student')
	sc_week = models.TextField()
	sc_num_of_cpl = models.CharField(max_length = 2)
	sc_level = models.TextField(null = True)