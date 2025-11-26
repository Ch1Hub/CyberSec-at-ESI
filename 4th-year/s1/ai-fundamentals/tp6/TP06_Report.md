# TP 06: Comparative Study of Clustering Algorithms on Real-World Data
## Fundamentals of Artificial Intelligence

**Student Name:** Chikhaoui Youcef Chihab Eddine
**Date:** November 25, 2025  
**Dataset:** Iris Dataset (Flower Measurements)

---

## 1. Executive Summary

This laboratory work presents a comparative analysis of two fundamental clustering algorithms—**K-means** and **Hierarchical Clustering**—applied to the Iris dataset. The study evaluates both methods using multiple metrics, visualizations, and statistical analyses to determine their effectiveness and suitability for clustering flower measurements.

**Key Findings:**
- Both algorithms successfully identified 3 natural clusters in the data
- K-means achieved a slightly higher silhouette score (0.4599 vs 0.4467)
- Agreement rate between methods: 48.67%
- Only 1 outlier detected (0.67% of data)
- K-means produced more balanced clusters; hierarchical clustering revealed natural hierarchical structure

---

## 2. Dataset Selection and Justification

### 2.1 Dataset Description
**Source:** UCI Machine Learning Repository (via scikit-learn)  
**Name:** Iris Dataset  
**Size:** 150 instances, 4 numeric features  

**Features:**
1. Sepal length (cm)
2. Sepal width (cm)
3. Petal length (cm)
4. Petal width (cm)

**Target:** 3 species of Iris flowers (setosa, versicolor, virginica)

### 2.2 Justification
The Iris dataset was selected for the following reasons:

✅ **Meets Requirements:**
- Contains 4 numeric features (> 3 required)
- Contains 150 instances (> 50 required)
- No categorical variables

✅ **Clustering Suitability:**
- Well-known natural groupings (3 species)
- No missing values
- Features are continuous measurements
- Ideal for distance-based clustering algorithms
- Allows validation against known ground truth

✅ **Practical Relevance:**
- Real-world botanical measurements
- Classic benchmark dataset for clustering analysis
- Enables comparison with established literature

---

## 3. Data Preprocessing

### 3.1 Missing Values Analysis
**Result:** No missing values detected in any column  
**Action:** No imputation required

### 3.2 Feature Scaling
**Method:** StandardScaler (Z-score normalization)  
**Formula:** z = (x - μ) / σ

**Results After Scaling:**
- Mean of all features: ~0
- Standard deviation of all features: 1

**Justification:** Standardization is essential for distance-based clustering algorithms to prevent features with larger ranges from dominating the distance calculations.

### 3.3 Feature Selection
**Selected Features:** All 4 features used for clustering
- Sepal length (cm)
- Sepal width (cm)
- Petal length (cm)
- Petal width (cm)

**Rationale:** All features contain valuable discriminatory information and contribute to cluster separation.

---

## 4. K-means Clustering Analysis

### 4.1 Methodology
**Algorithm:** K-means (Lloyd's algorithm)  
**Parameters:**
- K range tested: 2 to 10
- Random state: 42 (for reproducibility)
- n_init: 10 (multiple initializations)

### 4.2 Optimal K Selection

#### Elbow Method Analysis
The elbow plot shows the Within-Cluster Sum of Squares (WCSS) decreasing as K increases. A noticeable "elbow" appears around K=3, suggesting this as an optimal value.

#### Silhouette Score Analysis
**Silhouette Scores by K:**
- K=2: 0.5818 (highest)
- K=3: 0.4599 ⭐ (selected)
- K=4: 0.3662
- K=5: 0.3371
- K=6-10: Decreasing trend

**Selected K: 3**

**Justification:** While K=2 has the highest silhouette score, K=3 provides better interpretability and aligns with the known structure of the dataset (3 species). The score of 0.4599 indicates moderate cluster cohesion and separation.

### 4.3 K-means Results (K=3)

**Performance Metrics:**
- Silhouette Score: **0.4599**
- Cluster Distribution:
  - Cluster 0: 53 samples (35.3%)
  - Cluster 1: 50 samples (33.3%)
  - Cluster 2: 47 samples (31.3%)

**Cluster Characteristics:**

| Cluster | Sepal Length | Sepal Width | Petal Length | Petal Width | Interpretation |
|---------|-------------|-------------|--------------|-------------|----------------|
| 0       | 5.80        | 2.67        | 4.37         | 1.41        | Medium flowers |
| 1       | 5.01        | 3.43        | 1.46         | 0.25        | Small flowers  |
| 2       | 6.78        | 3.10        | 5.51         | 1.97        | Large flowers  |

**Key Observations:**
- Well-balanced cluster sizes (minimal variance)
- Clear separation based on flower size
- Cluster 1 (small flowers) is highly distinct
- Clusters 0 and 2 show some overlap

---

## 5. Hierarchical Clustering Analysis

### 5.1 Methodology
**Algorithm:** Agglomerative Hierarchical Clustering  
**Linkage Methods Tested:**
1. Single linkage
2. Complete linkage
3. Average linkage
4. Ward linkage

### 5.2 Dendrogram Analysis

Four dendrograms were generated for different linkage methods. Key observations:

**Single Linkage:**
- Tends to create chain-like clusters
- Sensitive to outliers
- Not optimal for this dataset

**Complete Linkage:**
- Creates compact, spherical clusters
- More resistant to outliers
- Shows clear 3-cluster structure

**Average Linkage:**
- Balanced approach between single and complete
- Moderate performance

**Ward Linkage:** ⭐ (Selected)
- Minimizes within-cluster variance
- Produces most balanced clusters
- Best silhouette scores across different K values

### 5.3 Optimal Parameters Selection

**Best Silhouette Scores by Linkage Method:**
- Single: K=2, Score=0.5270
- Complete: K=2, Score=0.5441
- Average: K=2, Score=0.5388
- **Ward: K=3, Score=0.4467** ⭐

**Selected Parameters:**
- Linkage: Ward
- K: 3

### 5.4 Hierarchical Clustering Results (Ward, K=3)

**Performance Metrics:**
- Silhouette Score: **0.4467**
- Cluster Distribution:
  - Cluster 0: 71 samples (47.3%)
  - Cluster 1: 49 samples (32.7%)
  - Cluster 2: 30 samples (20.0%)

**Cluster Characteristics:**

| Cluster | Sepal Length | Sepal Width | Petal Length | Petal Width | Interpretation |
|---------|-------------|-------------|--------------|-------------|----------------|
| 0       | 6.55        | 2.99        | 5.27         | 1.85        | Large flowers  |
| 1       | 5.02        | 3.45        | 1.47         | 0.24        | Small flowers  |
| 2       | 5.53        | 2.57        | 3.93         | 1.21        | Medium flowers |

**Key Observations:**
- Imbalanced cluster sizes (Cluster 0 largest, Cluster 2 smallest)
- Cluster 1 (small flowers) remains highly consistent
- Hierarchical relationships capture natural groupings
- More nuanced separation between medium and large flowers

---

## 6. Comparative Analysis

### 6.1 Cluster Assignment Comparison

**Cross-Tabulation of Cluster Assignments:**

|           | Hierarchical 0 | Hierarchical 1 | Hierarchical 2 |
|-----------|---------------|---------------|---------------|
| K-means 0 | 24            | 0             | 29            |
| K-means 1 | 0             | 49            | 1             |
| K-means 2 | 47            | 0             | 0             |

**Agreement Rate: 48.67%**

**Interpretation:**
- Only 48.67% of samples assigned to corresponding clusters
- Cluster 1 (small flowers) shows near-perfect agreement (49/50 samples)
- K-means clusters 0 and 2 are split differently by hierarchical clustering
- Different algorithms capture different aspects of data structure

### 6.2 Performance Comparison

| Metric                | K-means | Hierarchical |
|-----------------------|---------|--------------|
| Silhouette Score      | 0.4599  | 0.4467       |
| Cluster Balance       | High    | Low          |
| Most balanced cluster | 50      | 71           |
| Least balanced cluster| 47      | 30           |
| Variance in sizes     | Low     | High         |

**Winner by Metric:**
- ✅ Silhouette Score: K-means (+0.0132)
- ✅ Cluster Balance: K-means
- ✅ Interpretability: Hierarchical (dendrogram)

### 6.3 Visual Comparison

**Scatter Plot Analysis:**
When visualizing clusters using sepal length vs. sepal width:
- K-means: Creates more spherical, evenly-distributed clusters
- Hierarchical: Adapts better to natural data boundaries
- Both methods clearly separate small flowers from medium/large

**Box Plot Analysis:**
- Both methods show similar feature distributions within clusters
- K-means clusters have slightly tighter interquartile ranges
- Hierarchical clustering shows more overlap in boundary regions

### 6.4 Outlier Sensitivity

**Outlier Detection (Z-score > 3):**
- Total outliers: 1 (0.67%)
- K-means assignment: Cluster 1
- Hierarchical assignment: Cluster 1
- **Conclusion:** Both methods handled the outlier identically

**Sensitivity Assessment:**
- K-means: Moderately sensitive (centroids can shift)
- Hierarchical (Ward): Less sensitive due to variance minimization
- Both performed well on this clean dataset

---

## 7. Discussion and Insights

### 7.1 K-means Clustering

**Advantages Observed:**
✅ Faster computation (suitable for large datasets)  
✅ Produces balanced, spherical clusters  
✅ Higher silhouette score (better cohesion/separation)  
✅ Clear centroid-based interpretation  
✅ Consistent results with multiple runs (random_state=42)

**Limitations Observed:**
⚠️ Assumes spherical cluster shapes  
⚠️ Sensitive to initial centroid positions (mitigated with n_init=10)  
⚠️ Less flexible with non-convex clusters  
⚠️ Requires pre-specification of K  
⚠️ May struggle with clusters of very different sizes

**Best Use Cases:**
- Large datasets requiring efficiency
- When clusters are expected to be roughly spherical and similar in size
- When computational resources are limited
- When a specific number of clusters is desired

### 7.2 Hierarchical Clustering

**Advantages Observed:**
✅ No need to pre-specify number of clusters  
✅ Dendrogram provides rich visualization of data structure  
✅ Multiple linkage methods offer flexibility  
✅ Captures hierarchical relationships in data  
✅ Deterministic results (no random initialization)

**Limitations Observed:**
⚠️ More computationally expensive (O(n³) complexity)  
⚠️ Produced imbalanced clusters  
⚠️ Once merged, clusters cannot be separated  
⚠️ Single linkage very sensitive to outliers  
⚠️ Slightly lower silhouette score

**Best Use Cases:**
- Small to medium-sized datasets
- When exploring data structure and relationships
- When number of clusters is unknown
- When hierarchical relationships are meaningful
- When visualization of cluster formation is important

### 7.3 Method Suitability for Iris Dataset

**Recommendation: K-means** ⭐

**Justification:**
1. **Better Performance:** Higher silhouette score (0.4599 vs 0.4467)
2. **Balanced Clusters:** More even distribution aligns with known species distribution
3. **Interpretability:** Clear centroids correspond to "small," "medium," and "large" flower types
4. **Efficiency:** Faster execution for potential larger botanical datasets
5. **Robustness:** Minimal outliers make K-means initialization less problematic

**However, Hierarchical Has Merit:**
- Dendrogram reveals natural grouping structure
- Ward linkage captures variance-based relationships
- Useful for exploratory analysis before applying K-means

**Hybrid Approach Suggested:**
Use hierarchical clustering for initial exploration and determining K, then apply K-means for final clustering.

---

## 8. Limitations and Improvements

### 8.1 Current Limitations

**1. Feature Selection**
- Used all 4 features without dimensionality reduction
- Potential redundancy between correlated features
- 2D visualizations required selecting feature pairs

**2. Scaling Method**
- StandardScaler assumes normal distribution
- May not be optimal for skewed features

**3. Distance Metric**
- Used Euclidean distance exclusively
- May not capture all relationships

**4. Evaluation Metrics**
- Silhouette score is one of many validity indices
- No external validation against true labels (intentional for unsupervised learning)

**5. Cluster Validation**
- Limited cross-validation
- No stability analysis across multiple runs

### 8.2 Proposed Improvements

**1. Advanced Feature Engineering**
```
✓ Apply Principal Component Analysis (PCA) for dimensionality reduction
✓ Create feature ratios (e.g., petal_length/petal_width)
✓ Use feature importance from supervised models
```

**2. Alternative Scaling Methods**
```
✓ RobustScaler (less sensitive to outliers)
✓ MinMaxScaler (bounded normalization)
✓ PowerTransformer (handle non-normal distributions)
```

**3. Distance Metric Exploration**
```
✓ Manhattan distance (L1 norm)
✓ Cosine similarity
✓ Mahalanobis distance (accounts for correlations)
```

**4. Enhanced Validation**
```
✓ Davies-Bouldin Index (lower is better)
✓ Calinski-Harabasz Score (higher is better)
✓ Gap statistic for optimal K
✓ Adjusted Rand Index (compare with ground truth)
```

**5. Advanced Clustering Methods**
```
✓ DBSCAN (density-based, handles arbitrary shapes)
✓ Gaussian Mixture Models (soft clustering)
✓ Spectral Clustering (non-linear boundaries)
✓ OPTICS (varying density clusters)
```

**6. Robustness Testing**
```
✓ Bootstrap resampling for stability
✓ Cross-validation with different subsets
✓ Sensitivity analysis to parameter changes
```

---

## 9. Conclusions

This comparative study successfully demonstrated the application and evaluation of K-means and hierarchical clustering algorithms on the Iris dataset. Key conclusions:

### 9.1 Main Findings

1. **Both Algorithms Effective:** Both methods successfully identified 3 meaningful clusters corresponding to flower size categories (small, medium, large).

2. **K-means Superior Performance:** K-means achieved better quantitative results (silhouette score: 0.4599) and more balanced clusters.

3. **Hierarchical Provides Insights:** Dendrograms revealed hierarchical structure and validated K=3 as appropriate cluster count.

4. **Moderate Agreement:** 48.67% agreement rate indicates methods capture different aspects of data structure.

5. **Dataset Quality:** Clean dataset (only 0.67% outliers) allowed both algorithms to perform optimally.

### 9.2 Practical Recommendations

**For Production Use:**
- **Choose K-means** for final clustering (better performance, scalability)
- Use hierarchical clustering (Ward linkage) for initial K determination
- Validate results with multiple metrics, not just silhouette score

**For Research/Exploration:**
- Generate dendrograms to understand data relationships
- Compare multiple linkage methods
- Consider ensemble approaches combining both methods

### 9.3 Learning Outcomes

This laboratory successfully achieved the following:

✅ Sourced and justified appropriate real-world dataset  
✅ Performed comprehensive data preprocessing  
✅ Applied K-means with multiple K values and evaluation  
✅ Applied hierarchical clustering with multiple linkage methods  
✅ Generated dendrograms and cluster visualizations  
✅ Conducted comparative analysis with statistical evidence  
✅ Discussed method suitability and limitations  
✅ Proposed meaningful improvements  

---

## 10. Key Visualizations Summary

### Generated Visualizations:
1. ✅ Feature distributions (before/after scaling)
2. ✅ Elbow plot (K-means WCSS)
3. ✅ Silhouette score plots (K-means and hierarchical)
4. ✅ K-means cluster scatter plots (6 feature pairs)
5. ✅ Dendrograms (4 linkage methods)
6. ✅ Hierarchical cluster scatter plots (6 feature pairs)
7. ✅ Side-by-side comparison (K-means vs hierarchical)
8. ✅ Box plots (cluster characteristics by feature)

All visualizations are included in the Jupyter notebook: `clustering_analysis.ipynb`

---

## 11. References

**Dataset Source:**
- Fisher, R.A. (1936). "The use of multiple measurements in taxonomic problems." *Annals of Eugenics*, 7(2), 179-188.
- UCI Machine Learning Repository: https://archive.ics.uci.edu/ml/datasets/iris

**Libraries Used:**
- NumPy 1.x
- Pandas 2.x
- Matplotlib 3.x
- Seaborn 0.x
- Scikit-learn 1.x
- SciPy 1.x

**Algorithms:**
- MacQueen, J. (1967). "Some methods for classification and analysis of multivariate observations."
- Ward, J.H. (1963). "Hierarchical grouping to optimize an objective function."

---

## Appendix: Technical Implementation Details

**Environment:**
- Python 3.x
- Jupyter Notebook
- VS Code

**Reproducibility:**
- Random seed: 42
- All code available in: `clustering_analysis.ipynb`
- Complete execution from top to bottom

**Data Availability:**
- Dataset: Built-in with scikit-learn (sklearn.datasets.load_iris)
- No external downloads required

---

**End of Report**
