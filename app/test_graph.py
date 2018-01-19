import matplotlib
matplotlib.use('Agg')




import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import statistics as stats



objects = ('2018-05-05', '2018-06-05', '2018-07-05', '2018-08-05', '2018-09-05', '2018-10-05')
y_pos = np.arange(len(objects))
cloud_percent = [30, 10, 25, 16, 18, 50]
 
barlist = plt.bar(y_pos, cloud_percent, align='center', alpha=0.5)

for i in barlist:
    if i.get_height() > 25:
        i.set_color('r')
    else:
        i.set_color('g')




plt.xticks(y_pos, objects, rotation=45)
plt.ylabel('% of cloud cover')
plt.xlabel('Image acquition dates')
plt.title('Sentinel 2A images cloud cover')

x = stats.mean(cloud_percent)
y = stats.median(cloud_percent)
a = stats.stdev(cloud_percent)
b = stats.variance(cloud_percent)


cloud_stats = """mean     :"""+format(x, '.2f')+"""
median  :"""+format(y, '.2f')+"""
stdev     :"""+format(a, '.2f')+"""
variance:"""+format(b, '.2f')+""" """


plt.axhline(y=25, color='b', linestyle='-')


plt.text(6,30,cloud_stats, fontsize=20)
 
plt.savefig('bar_graph.png', bbox_inches="tight")









