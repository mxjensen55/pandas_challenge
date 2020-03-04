#!/usr/bin/env python
# coding: utf-8

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[1]:


# Dependencies and Setup
import pandas as pd
import numpy as np

# File to Load (Remember to Change These)
school_data_to_load = "Resources/schools_complete.csv"
student_data_to_load = "Resources/students_complete.csv"

# Read School and Student Data File and store into Pandas Data Frames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])


# In[2]:


school_data_complete.head(10)


# In[3]:


school_count=len(school_data_complete["school_name"].unique())
number_of_students=(school_data_complete["student_name"].count())
total_budget=school_data["budget"].sum()
average_math=(school_data_complete["math_score"].sum())/(school_data_complete["math_score"].count())
average_reading=(school_data_complete["reading_score"].sum())/(school_data_complete["reading_score"].count())
num_pass_math=len(school_data_complete.loc[school_data_complete["math_score"]>=70])
percent_pass_math=(num_pass_math/number_of_students*100)
num_pass_reading=len(school_data_complete.loc[school_data_complete["reading_score"]>=70])
percent_pass_reading=((num_pass_reading)/(number_of_students)*100)
overall_pass=(percent_pass_math+percent_pass_reading)/2


# # District Summary
# 
# * Calculate the total number of schools
# 
# * Calculate the total number of students
# 
# * Calculate the total budget
# 
# * Calculate the average math score 
# 
# * Calculate the average reading score
# 
# * Calculate the overall passing rate (overall average score), i.e. (avg. math score + avg. reading score)/2
# 
# * Calculate the percentage of students with a passing math score (70 or greater)
# 
# * Calculate the percentage of students with a passing reading score (70 or greater)
# 
# * Create a dataframe to hold the above results
# 
# * Optional: give the displayed data cleaner formatting

# In[4]:


summary_table=pd.DataFrame({"Total Schools": school_count,
                           "Total Students": number_of_students,
                           "Total Budget": total_budget,
                           "Average Math Score": average_math,
                            "Average Reading Score": average_reading,
                            "% Passing Math": percent_pass_math,
                            "% Passing Reading": percent_pass_reading,
                           "% Overall Passing Rate": overall_pass
                           }, 
                           index=[0])
summary_table["Total Budget"]=summary_table["Total Budget"].map("${:,}".format)
summary_table["Total Students"]=summary_table["Total Students"].map("{:,}".format)

summary_table


# ## School Summary

# * Create an overview table that summarizes key metrics about each school, including:
#   * School Name
#   * School Type
#   * Total Students
#   * Total School Budget
#   * Per Student Budget
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * Overall Passing Rate (Average of the above two)
#   
# * Create a dataframe to hold the above results

# ## Top Performing Schools (By Passing Rate)

# In[10]:


school_type = school_data_complete.set_index(['school_name'])
school_type = school_type.groupby(['school_name','type']).count()
school_type = school_type.reset_index().set_index('school_name')['type']

school_type


# In[11]:


per_school_count=school_data_complete["school_name"].value_counts()
total_school_budget=school_data_complete.groupby(["school_name"]).mean()["budget"]
per_student_budget=total_school_budget/per_school_count
avg_math_score=school_data_complete.groupby(['school_name']).mean()["math_score"]
avg_reading_score=school_data_complete.groupby(['school_name']).mean()["reading_score"]
num_pass_maths=school_data_complete[(school_data_complete["math_score"]>=70)]
per_school_passing_math=num_pass_maths.groupby(["school_name"]).count()["student_name"]/per_school_count*100
num_pass_readings=school_data_complete[(school_data_complete["reading_score"]>=70)]
per_school_passing_reading=num_pass_readings.groupby(["school_name"]).count()["student_name"]/per_school_count*100
overall_pass_by_school=(per_school_passing_math+per_school_passing_reading)/2

school_summary=pd.DataFrame({
                            "School Type": school_type,
                             "Total Students": per_school_count,
                             "Total School Budget": total_school_budget,
                             "Per Student Budget": per_student_budget,
                             "Average Math Score": avg_math_score,
                             "Average Reading Score": avg_reading_score,
                             "% Passing Math": per_school_passing_math,
                             "% Passing Reading": per_school_passing_reading,
                             "% Overall Passing Rate": overall_pass_by_school
                            })

school_summary["Total School Budget"]=school_summary["Total School Budget"].map("${:,}".format)
#school_summary["Per Student Budget"]=school_summary["Per Student Budget"].map("${:,}".format)
best_schools=school_summary.sort_values(["% Overall Passing Rate"], ascending=False)

best_schools.head(5)


# * Sort and display the top five schools in overall passing rate

# ## Bottom Performing Schools (By Passing Rate)

# In[12]:


worst_schools=school_summary.sort_values(["% Overall Passing Rate"], ascending=True)
worst_schools.head(5)


# * Sort and display the five worst-performing schools

# ## Math Scores by Grade

# * Create a table that lists the average Reading Score for students of each grade level (9th, 10th, 11th, 12th) at each school.
# 
#   * Create a pandas series for each grade. Hint: use a conditional statement.
#   
#   * Group each series by school
#   
#   * Combine the series into a dataframe
#   
#   * Optional: give the displayed data cleaner formatting

# In[13]:


ninth_grader=school_data_complete[(school_data_complete["grade"]=="9th")]
tenth_grader=school_data_complete[(school_data_complete["grade"]=="10th")]
eleventh_grader=school_data_complete[(school_data_complete["grade"]=="11th")]
twelth_grader=school_data_complete[(school_data_complete["grade"]=="12th")]
avg_math_ninth=ninth_grader.groupby(["school_name"]).mean()["math_score"]
avg_math_tenth=tenth_grader.groupby(["school_name"]).mean()["math_score"]
avg_math_eleventh=eleventh_grader.groupby(["school_name"]).mean()["math_score"]
avg_math_twelth=twelth_grader.groupby(["school_name"]).mean()["math_score"]

summary_math_by_grade=pd.DataFrame({"9th": avg_math_ninth,
                              "10th": avg_math_tenth,
                              "11th": avg_math_eleventh,
                              "12th": avg_math_twelth})

summary_math_by_grade.index.name=None

summary_math_by_grade


# In[14]:


avg_read_ninth=ninth_grader.groupby(["school_name"]).mean()["reading_score"]
avg_read_tenth=tenth_grader.groupby(["school_name"]).mean()["reading_score"]
avg_read_eleventh=eleventh_grader.groupby(["school_name"]).mean()["reading_score"]
avg_read_twelth=twelth_grader.groupby(["school_name"]).mean()["reading_score"]


# ## Reading Score by Grade 

# * Perform the same operations as above for reading scores

# In[15]:


summary_reading_by_grade=pd.DataFrame({"9th": avg_read_ninth,
                              "10th": avg_read_tenth,
                              "11th": avg_read_eleventh,
                              "12th": avg_read_twelth})

summary_reading_by_grade.index.name=None

summary_reading_by_grade


# ## Scores by School Spending

# * Create a table that breaks down school performances based on average Spending Ranges (Per Student). Use 4 reasonable bins to group school spending. Include in the table each of the following:
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * Overall Passing Rate (Average of the above two)

# In[16]:


school_summary.astype({'Per Student Budget': 'int64'}).dtypes


# In[17]:


per_student_budget


# In[18]:


# Sample bins. Feel free to create your own bins.
spending_bins = [0, 585, 615, 645, 675]
group_names = ["<$585", "$585-615", "$615-645", "$645-675"]


# In[19]:


school_summary["Spending Ranges(Per Student)"]=pd.cut(school_summary["Per Student Budget"], spending_bins, labels=group_names)
school_summary.head()


# In[20]:


avg_math_by_spending=school_summary.groupby(["Spending Ranges(Per Student)"]).mean()["Average Math Score"]
avg_reading_by_spending=school_summary.groupby(["Spending Ranges(Per Student)"]).mean()["Average Reading Score"]
passing_math_by_spending=school_summary.groupby(["Spending Ranges(Per Student)"]).mean()["% Passing Math"]
passing_reading_by_spending=school_summary.groupby(["Spending Ranges(Per Student)"]).mean()["% Passing Reading"]
overall_pass_by_spending=school_summary.groupby(["Spending Ranges(Per Student)"]).mean()["% Overall Passing Rate"]

summary_by_spending=pd.DataFrame({"Average Math Score": avg_math_by_spending,
                                 "Average Reading Score": avg_reading_by_spending,
                                 "% Passing Math": passing_math_by_spending,
                                 "% Passing Reading": passing_reading_by_spending,
                                 "% Overall Passing Rate": overall_pass_by_spending})

summary_by_spending.index.name=None

summary_by_spending


# ## Scores by School Size

# * Perform the same operations as above, based on school size.

# In[21]:


# Sample bins. Feel free to create your own bins.
size_bins = [0, 1000, 2000, 5000]
group_names = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]


# In[22]:


school_summary["School Size"]=pd.cut(school_summary["Total Students"], size_bins, labels=group_names)
school_summary.head()


# In[23]:


avg_math_by_size=school_summary.groupby(["School Size"]).mean()["Average Math Score"]
avg_reading_by_size=school_summary.groupby(["School Size"]).mean()["Average Reading Score"]
passing_math_by_size=school_summary.groupby(["School Size"]).mean()["% Passing Math"]
passing_reading_by_size=school_summary.groupby(["School Size"]).mean()["% Passing Reading"]
overall_pass_by_size=school_summary.groupby(["School Size"]).mean()["% Overall Passing Rate"]

summary_by_size=pd.DataFrame({"Average Math Score":avg_math_by_size,
                             "Average Reading Score": avg_reading_by_size,
                             "% Passing Math": passing_math_by_size,
                             "% Passing Reading": passing_reading_by_size,
                             "% Overall Passing Rate": overall_pass_by_size})
summary_by_size.index.name=None

summary_by_size


# ## Scores by School Type

# * Perform the same operations as above, based on school type.

# In[25]:


avg_math_by_type=school_summary.groupby(["School Type"]).mean()["Average Math Score"]
avg_reading_by_type=school_summary.groupby(["School Type"]).mean()["Average Reading Score"]
passing_math_by_type=school_summary.groupby(["School Type"]).mean()["% Passing Math"]
passing_reading_by_type=school_summary.groupby(["School Type"]).mean()["% Passing Reading"]
overall_pass_by_type=school_summary.groupby(["School Type"]).mean()["% Overall Passing Rate"]

summary_by_type=pd.DataFrame({"Average Math Score": avg_math_by_type,
                             "Average Reading Score": avg_reading_by_type,
                             "% Passing Math": passing_math_by_type,
                             "% Passing Reading":passing_reading_by_type,
                             "% Overall Passing Rate": overall_pass_by_type })
summary_by_type.index.name=None

summary_by_type


# In[ ]:




