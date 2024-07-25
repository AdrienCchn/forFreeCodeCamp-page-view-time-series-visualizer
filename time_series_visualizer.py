import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
DATA_FILENAME = "fcc-forum-pageviews.csv"
df = pd.read_csv(f"{DATA_FILENAME}", sep=",", skipinitialspace=True)

# Clean data
df_temp = df.copy()
df_temp = df_temp[(df_temp['value'] >= df['value'].quantile(0.025))]
df_temp = df_temp[(df_temp['value'] <= df['value'].quantile(1 - 0.025))]
df = df_temp.copy()

df["date"] = pd.to_datetime(df["date"])


months_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

months_short_list = []
for word in range(len(months_list)):
    months_short_list.append(months_list[word][0:3])


ticks_list_label = ["0", "20000", "40000", "60000", "80000", "100000", "120000", "140000", "160000", "180000", "200000"]
ticks_list_int = [int(s) for s in ticks_list]



def draw_line_plot():
    df_line = df.copy()
    df_line = df_line.set_index("date")

    # Draw line plot
    fig, ax = plt.subplots(figsize=(19, 6))

    ax.plot(df_line.index, df_line["value"], color="red")
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019", fontsize=15)
    plt.xlabel("Date", fontsize=13)
    plt.ylabel("Page Views", fontsize=13)
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig



def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar["year"] = df_bar["date"].dt.year
    df_bar["month"] = df_bar["date"].dt.month
    
    df_bar_pivot = df_bar.pivot_table(index=["year", "month"], values="value", aggfunc="mean")
    df_bar_pivot = df_bar_pivot.reset_index()


    # Draw bar plot
    fig, ax = plt.subplots(figsize=(9, 9))
    ax = sns.barplot(data=df_bar_pivot, x="year", y="value", hue="month", palette="tab10")
    plt.xlabel("Years", fontsize=14)
    plt.ylabel("Average Page Views", fontsize=14)
    plt.xticks(fontsize=13, rotation=90)
    plt.yticks(fontsize=13)
    h, l = ax.get_legend_handles_labels()
    ax.legend(h, months_list, title="Months", loc="upper left", fontsize=14, title_fontsize=14)


    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig



def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(28.80, 10.80), sharey=True)
    plt.gcf().subplots_adjust(left = 0.05, bottom = 0.07, right = 0.95, top = 0.93, wspace = 0.15, hspace = 0)
    
    plt.subplot(1,2,1)
    axes[0] = sns.boxplot(data=df_box, x="year", y="value", hue="year", palette="tab10", linewidth=1, width=0.80, fliersize=2, dodge=False).get_legend().remove()
    plt.title("Year-wise Box Plot (Trend)", fontsize=19)
    plt.xlabel("Year", fontsize=15)
    plt.ylabel("Page Views", fontsize=15)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15, ticks=ticks_list_int, labels=ticks_list_label)
    
    plt.subplot(1,2,2)
    axes[1] = sns.boxplot(data=df_box, x="month", y="value", hue="month", palette="rainbow", linewidth=1, width=0.75, fliersize=2, dodge=False, order=months_short_list).get_legend().remove()
    plt.title("Month-wise Box Plot (Seasonality)", fontsize=19)
    plt.xlabel("Month", fontsize=15)
    plt.ylabel("Page Views", fontsize=15)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15, ticks=ticks_list_int, labels=ticks_list_label)

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
