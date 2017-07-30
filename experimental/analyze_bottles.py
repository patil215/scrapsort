import vision
import operator

label_counts = {}
label_score_totals = {}

for i in range(0, 45):
    labels = vision.get_image_labels("img/bottles/bottle%d.jpg" % i)
    for label in labels:
        description = label.get("description")
        score = label.get("score")

        label_counts[description] = label_counts.get(description, 0) + 1
        label_score_totals[description] = label_score_totals.get(description, 0) + score
        
    print "Analyzed bottle %d" % i

sorted_label_counts = sorted(label_counts.items(), key=operator.itemgetter(1))
for pair in sorted_label_counts:
    print("Label: %s" % pair[0])
    print("Count: %d" % pair[1])
    average = label_score_totals.get(pair[0]) / pair[1]
    print("Average Score: %f" % average)
    print
