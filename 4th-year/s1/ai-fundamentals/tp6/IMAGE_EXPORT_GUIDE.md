# Image Export Guide for TP06 LaTeX Report

## 📸 Complete Image Export Instructions

Add the `plt.savefig()` line **BEFORE** `plt.show()` in each plotting cell. Here's the exact code for each image:

---

## Image 1: Feature Distributions (Before/After Scaling)

**Location**: Cell 11 - After the histogram plotting code

```python
# Visualize feature distributions before and after scaling
fig, axes = plt.subplots(2, 4, figsize=(16, 8))

for i, feature in enumerate(features_to_use):
    axes[0, i].hist(X[:, i], bins=30, edgecolor='black', alpha=0.7)
    axes[0, i].set_title(f'{feature}\n(Original)')
    axes[0, i].set_ylabel('Frequency')
    
    axes[1, i].hist(X_scaled[:, i], bins=30, edgecolor='black', alpha=0.7)
    axes[1, i].set_title(f'{feature}\n(Scaled)')
    axes[1, i].set_ylabel('Frequency')

plt.tight_layout()
plt.suptitle('Feature Distributions: Original vs Scaled', y=1.02, fontsize=14, fontweight='bold')

# ✅ ADD THIS LINE:
plt.savefig('feature_distributions.png', dpi=300, bbox_inches='tight')

plt.show()
```

---

## Image 2: Elbow Method and Silhouette Scores

**Location**: Cell 14 - After K-means evaluation plots

```python
# Plot Elbow Method and Silhouette Scores
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Elbow plot
ax1.plot(K_range, inertias, 'bo-', linewidth=2, markersize=8)
ax1.set_xlabel('Number of Clusters (K)', fontsize=12)
ax1.set_ylabel('Within-Cluster Sum of Squares (Inertia)', fontsize=12)
ax1.set_title('Elbow Method', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)

# Silhouette score plot
ax2.plot(K_range, silhouette_scores, 'ro-', linewidth=2, markersize=8)
ax2.set_xlabel('Number of Clusters (K)', fontsize=12)
ax2.set_ylabel('Silhouette Score', fontsize=12)
ax2.set_title('Silhouette Score Analysis', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3)

plt.tight_layout()

# ✅ ADD THIS LINE:
plt.savefig('elbow_silhouette.png', dpi=300, bbox_inches='tight')

plt.show()

# Print silhouette scores
print("\nSilhouette Scores for different K values:")
for k, score in zip(K_range, silhouette_scores):
    print(f"K = {k}: {score:.4f}")
```

---

## Image 3: K-means Cluster Visualization

**Location**: Cell 18 - K-means cluster scatter plots (6 feature pairs)

```python
# 2D visualization using first two features
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.ravel()

# Plot all feature pairs
plot_idx = 0
for i in range(len(features_to_use)):
    for j in range(i+1, len(features_to_use)):
        if plot_idx < 6:
            scatter = axes[plot_idx].scatter(X_scaled[:, i], X_scaled[:, j], 
                                            c=kmeans_labels, cmap='viridis', 
                                            alpha=0.6, s=50, edgecolors='k', linewidth=0.5)
            axes[plot_idx].set_xlabel(features_to_use[i], fontsize=10)
            axes[plot_idx].set_ylabel(features_to_use[j], fontsize=10)
            axes[plot_idx].set_title(f'K-means Clusters\n{features_to_use[i]} vs {features_to_use[j]}', 
                                    fontsize=11, fontweight='bold')
            axes[plot_idx].grid(True, alpha=0.3)
            plot_idx += 1

plt.colorbar(scatter, ax=axes, label='Cluster')
plt.tight_layout()

# ✅ ADD THIS LINE:
plt.savefig('kmeans_clusters.png', dpi=300, bbox_inches='tight')

plt.show()
```

---

## Image 4: Dendrograms (4 Linkage Methods)

**Location**: Cell 22 - Dendrogram plots

```python
# Plot dendrograms for different linkage methods
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
axes = axes.ravel()

for idx, method in enumerate(linkage_methods):
    dendrogram(linkage_matrices[method], ax=axes[idx], truncate_mode='lastp', p=30)
    axes[idx].set_title(f'Dendrogram - {method.capitalize()} Linkage', 
                       fontsize=14, fontweight='bold')
    axes[idx].set_xlabel('Sample Index or (Cluster Size)', fontsize=11)
    axes[idx].set_ylabel('Distance', fontsize=11)
    axes[idx].grid(True, alpha=0.3)

plt.tight_layout()

# ✅ ADD THIS LINE:
plt.savefig('dendrograms.png', dpi=300, bbox_inches='tight')

plt.show()
```

---

## Image 5: Hierarchical Clustering Silhouette Scores

**Location**: Cell 26 - Hierarchical clustering evaluation plot

```python
# Plot silhouette scores for different linkage methods
plt.figure(figsize=(12, 6))

for method in linkage_methods:
    plt.plot(n_clusters_range, hierarchical_scores[method], 'o-', 
            label=f'{method.capitalize()} Linkage', linewidth=2, markersize=8)

plt.xlabel('Number of Clusters', fontsize=12)
plt.ylabel('Silhouette Score', fontsize=12)
plt.title('Hierarchical Clustering: Silhouette Score Comparison', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()

# ✅ ADD THIS LINE:
plt.savefig('hierarchical_silhouette.png', dpi=300, bbox_inches='tight')

plt.show()

# Print best scores for each method
print("\nBest Silhouette Scores:")
for method in linkage_methods:
    best_idx = np.argmax(hierarchical_scores[method])
    best_k = list(n_clusters_range)[best_idx]
    best_score = hierarchical_scores[method][best_idx]
    print(f"{method.capitalize()} Linkage: K = {best_k}, Score = {best_score:.4f}")
```

---

## Image 6: Hierarchical Cluster Visualization

**Location**: Cell 29 - Hierarchical cluster scatter plots (6 feature pairs)

```python
# 2D visualization of hierarchical clusters
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.ravel()

# Plot all feature pairs
plot_idx = 0
for i in range(len(features_to_use)):
    for j in range(i+1, len(features_to_use)):
        if plot_idx < 6:
            scatter = axes[plot_idx].scatter(X_scaled[:, i], X_scaled[:, j], 
                                            c=hier_labels, cmap='plasma', 
                                            alpha=0.6, s=50, edgecolors='k', linewidth=0.5)
            axes[plot_idx].set_xlabel(features_to_use[i], fontsize=10)
            axes[plot_idx].set_ylabel(features_to_use[j], fontsize=10)
            axes[plot_idx].set_title(f'Hierarchical Clusters ({best_linkage})\n{features_to_use[i]} vs {features_to_use[j]}', 
                                    fontsize=11, fontweight='bold')
            axes[plot_idx].grid(True, alpha=0.3)
            plot_idx += 1

plt.colorbar(scatter, ax=axes, label='Cluster')
plt.tight_layout()

# ✅ ADD THIS LINE:
plt.savefig('hierarchical_clusters.png', dpi=300, bbox_inches='tight')

plt.show()
```

---

## Image 7: Side-by-Side Comparison (K-means vs Hierarchical)

**Location**: Cell 32 - Comparison visualization

```python
# Visualize cluster comparison
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# K-means
scatter1 = axes[0].scatter(X_scaled[:, 0], X_scaled[:, 1], 
                          c=kmeans_labels, cmap='viridis', 
                          alpha=0.6, s=50, edgecolors='k', linewidth=0.5)
axes[0].set_xlabel(features_to_use[0], fontsize=12)
axes[0].set_ylabel(features_to_use[1], fontsize=12)
axes[0].set_title(f'K-means Clustering (K={optimal_k})', fontsize=14, fontweight='bold')
axes[0].grid(True, alpha=0.3)
plt.colorbar(scatter1, ax=axes[0], label='Cluster')

# Hierarchical
scatter2 = axes[1].scatter(X_scaled[:, 0], X_scaled[:, 1], 
                          c=hier_labels, cmap='plasma', 
                          alpha=0.6, s=50, edgecolors='k', linewidth=0.5)
axes[1].set_xlabel(features_to_use[0], fontsize=12)
axes[1].set_ylabel(features_to_use[1], fontsize=12)
axes[1].set_title(f'Hierarchical Clustering ({best_linkage}, K={optimal_hier_k})', 
                 fontsize=14, fontweight='bold')
axes[1].grid(True, alpha=0.3)
plt.colorbar(scatter2, ax=axes[1], label='Cluster')

plt.tight_layout()

# ✅ ADD THIS LINE:
plt.savefig('comparison_plot.png', dpi=300, bbox_inches='tight')

plt.show()
```

---

## Image 8: Box Plots (Cluster Characteristics Comparison)

**Location**: Cell 35 - Box plots for cluster characteristics

```python
# Box plots to compare cluster characteristics
fig, axes = plt.subplots(2, 4, figsize=(18, 10))

for idx, feature in enumerate(features_to_use):
    # K-means
    df_with_clusters.boxplot(column=feature, by='KMeans_Cluster', ax=axes[0, idx])
    axes[0, idx].set_title(f'K-means\n{feature}')
    axes[0, idx].set_xlabel('Cluster')
    axes[0, idx].set_ylabel('Value')
    
    # Hierarchical
    df_with_clusters.boxplot(column=feature, by='Hierarchical_Cluster', ax=axes[1, idx])
    axes[1, idx].set_title(f'Hierarchical\n{feature}')
    axes[1, idx].set_xlabel('Cluster')
    axes[1, idx].set_ylabel('Value')

plt.suptitle('Cluster Characteristics Comparison', fontsize=16, fontweight='bold', y=1.00)
plt.tight_layout()

# ✅ ADD THIS LINE:
plt.savefig('boxplots.png', dpi=300, bbox_inches='tight')

plt.show()
```

---

## 📥 Quick Download Method for Google Colab

If you're using **Google Colab**, add this cell at the very end to download all 8 images at once:

```python
# Download all images from Google Colab
from google.colab import files
import os

# List of all image files
image_files = [
    'feature_distributions.png',
    'elbow_silhouette.png',
    'kmeans_clusters.png',
    'dendrograms.png',
    'hierarchical_silhouette.png',
    'hierarchical_clusters.png',
    'comparison_plot.png',
    'boxplots.png'
]

# Download each image
for img in image_files:
    if os.path.exists(img):
        files.download(img)
        print(f"✅ Downloaded: {img}")
    else:
        print(f"❌ Not found: {img}")
```

---

## 📦 Alternative: Download as ZIP (Google Colab)

```python
# Create a ZIP file with all images
import shutil
import os
from google.colab import files

# Create images folder
os.makedirs('images', exist_ok=True)

# List of all image files
image_files = [
    'feature_distributions.png',
    'elbow_silhouette.png',
    'kmeans_clusters.png',
    'dendrograms.png',
    'hierarchical_silhouette.png',
    'hierarchical_clusters.png',
    'comparison_plot.png',
    'boxplots.png'
]

# Copy images to folder
for img in image_files:
    if os.path.exists(img):
        shutil.copy(img, f'images/{img}')
        print(f"✅ Copied: {img}")

# Create ZIP
shutil.make_archive('tp06_images', 'zip', 'images')
print("\n📦 Creating ZIP file...")

# Download ZIP
files.download('tp06_images.zip')
print("✅ Download complete! Extract the ZIP and upload to Overleaf.")
```

---

## ✅ Checklist

After running all cells with `plt.savefig()`:

- [ ] feature_distributions.png (Cell 11)
- [ ] elbow_silhouette.png (Cell 14)
- [ ] kmeans_clusters.png (Cell 18)
- [ ] dendrograms.png (Cell 22)
- [ ] hierarchical_silhouette.png (Cell 26)
- [ ] hierarchical_clusters.png (Cell 29)
- [ ] comparison_plot.png (Cell 32)
- [ ] boxplots.png (Cell 35)

---

## 💡 Pro Tips

1. **Run cells in order** - Make sure you execute cells sequentially from top to bottom
2. **Check file names** - Names must match exactly (case-sensitive)
3. **High quality** - `dpi=300` ensures publication-quality images
4. **Tight layout** - `bbox_inches='tight'` removes extra whitespace
5. **Verify downloads** - Check that all 8 files are in your downloads folder

---

## 🚀 Next Steps

1. ✅ Add `plt.savefig()` to all 8 plotting cells
2. ✅ Run all cells from top to bottom
3. ✅ Download all 8 PNG files
4. ✅ Upload to Overleaf in `images/` folder
5. ✅ Compile LaTeX document
6. ✅ Download PDF - Ready to submit! 🎓
