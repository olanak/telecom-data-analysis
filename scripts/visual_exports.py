import matplotlib.pyplot as plt
import seaborn as sns
import os


# Ensure the plots directory is created at the project root
plot_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../plots'))
os.makedirs(plot_dir, exist_ok=True)


def export_visualizations(top_handsets, top_manufacturers, user_data_cleaned, decile_aggregation, correlation_matrix, segmented_data):
    """
    Export various visualizations to the plots directory.

    Args:
        top_handsets (DataFrame): Top 10 handsets data.
        top_manufacturers (DataFrame): Top 3 manufacturers data.
        user_data_cleaned (DataFrame): Cleaned user data.
        decile_aggregation (DataFrame): Aggregated data by decile class.
        correlation_matrix (DataFrame): Correlation matrix of application usage.
        segmented_data (DataFrame): Data with PCA components.
    """

    ### Top 10 Handsets
    try:
        plt.figure(figsize=(10, 6))
        plt.bar(top_handsets['Handset Type'], top_handsets['count'])
        plt.title('Top 10 Handsets')
        plt.xticks(rotation=45, ha='right')
        plt.ylabel('Count')
        plt.tight_layout()
        plt.savefig(os.path.join(plot_dir, 'top_10_handsets.png'))
        plt.close()
        print("Top 10 Handsets plot exported.")
    except Exception as e:
        print(f"Error exporting Top 10 Handsets plot: {e}")


    ### Market Share by Manufacturer
    try:
        plt.figure(figsize=(8, 5))
        plt.pie(
            top_manufacturers['count'],
            labels=top_manufacturers['Handset Manufacturer'],
            autopct='%1.1f%%'
        )
        plt.title('Market Share by Manufacturer')
        plt.tight_layout()
        plt.savefig(os.path.join(plot_dir, 'manufacturer_share.png'))
        plt.close()
        print("Manufacturer market share plot exported.")
    except Exception as e:
        print(f"Error exporting manufacturer share plot: {e}")


    ### User Session Count Distribution
    try:
        plt.figure(figsize=(10, 6))
        plt.hist(user_data_cleaned['session_count'], bins=30, color='skyblue', edgecolor='black')
        plt.title('Distribution of Session Counts per User')
        plt.xlabel('Number of Sessions')
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.savefig(os.path.join(plot_dir, 'session_distribution.png'))
        plt.close()
        print("User session distribution plot exported.")
    except Exception as e:
        print(f"Error exporting session distribution plot: {e}")


    ### Data Volume by Decile Class
    try:
        plt.figure(figsize=(10, 6))
        plt.bar(decile_aggregation['decile_class'], decile_aggregation['total_data'])
        plt.title('Total Data Volume by Decile Class')
        plt.xlabel('Decile Class')
        plt.ylabel('Total Data Volume (Bytes)')
        plt.tight_layout()
        plt.savefig(os.path.join(plot_dir, 'data_by_decile.png'))
        plt.close()
        print("Data volume by decile plot exported.")
    except Exception as e:
        print(f"Error exporting decile class plot: {e}")


    ### Correlation Matrix (Heatmap)
    if not correlation_matrix.empty:
        try:
            plt.figure(figsize=(12, 8))
            sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
            plt.title('Correlation Matrix')
            plt.tight_layout()
            plt.savefig(os.path.join(plot_dir, 'correlation_matrix.png'))
            plt.close()
            print("Correlation matrix plot exported.")
        except Exception as e:
            print(f"Error exporting correlation matrix plot: {e}")
    else:
        print("No correlation matrix plot generated (empty matrix).")


    ### PCA Scatter Plot
    try:
        plt.figure(figsize=(8, 6))
        plt.scatter(segmented_data['PCA1'], segmented_data['PCA2'], alpha=0.5)
        plt.title("PCA: 2 Principal Components")
        plt.xlabel("PCA1")
        plt.ylabel("PCA2")
        plt.grid()
        plt.tight_layout()
        plt.savefig(os.path.join(plot_dir, 'pca_scatter.png'))
        plt.close()
        print("PCA scatter plot exported.")
    except Exception as e:
        print(f"Error exporting PCA scatter plot: {e}")

