import matplotlib.pyplot as plt



def generate_stats_chart(data, user_id):
    labels = [row[0] for row in data]
    number = [row[1] for row in data]
    plt.figure(figsize=(10, 6))
    plt.pie(number, labels=labels, autopct='%1.1f%%')
    name = f"{user_id}.png"
    plt.savefig(name)
    plt.close()
    return name