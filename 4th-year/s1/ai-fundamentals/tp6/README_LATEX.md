# TP06 LaTeX Report - Overleaf Setup Guide

## 🌐 Using Overleaf (Recommended - No Local Installation Needed!)

### Step 1: Create Overleaf Account
1. Go to **https://www.overleaf.com**
2. Click "Register" (free account is sufficient)
3. Sign up with your email or Google account
4. Verify your email

### Step 2: Export Images from Google Colab/Jupyter Notebook

You need to save 8 plots from your notebook. Add this code to save each plot:

```python
# For feature distributions plot (Cell 11):
plt.savefig('feature_distributions.png', dpi=300, bbox_inches='tight')
plt.show()

# For elbow and silhouette plot (Cell 14):
plt.savefig('elbow_silhouette.png', dpi=300, bbox_inches='tight')
plt.show()

# For K-means clusters (Cell 18):
plt.savefig('kmeans_clusters.png', dpi=300, bbox_inches='tight')
plt.show()

# For dendrograms (Cell 22):
plt.savefig('dendrograms.png', dpi=300, bbox_inches='tight')
plt.show()

# For hierarchical silhouette (Cell 26):
plt.savefig('hierarchical_silhouette.png', dpi=300, bbox_inches='tight')
plt.show()

# For hierarchical clusters (Cell 29):
plt.savefig('hierarchical_clusters.png', dpi=300, bbox_inches='tight')
plt.show()

# For comparison plot (Cell 32):
plt.savefig('comparison_plot.png', dpi=300, bbox_inches='tight')
plt.show()

# For box plots (Cell 35):
plt.savefig('boxplots.png', dpi=300, bbox_inches='tight')
plt.show()
```

**Download all 8 images** to your computer (they'll be in your Colab Files or Jupyter notebook directory).

### Step 3: Create New Overleaf Project

1. **Login to Overleaf**: https://www.overleaf.com
2. Click **"New Project"** (green button)
3. Select **"Blank Project"**
4. Name it: **"TP06_Clustering_Report"**
5. Click **"Create"**

### Step 4: Upload LaTeX File

1. In your new Overleaf project, you'll see a file called `main.tex`
2. **Delete** the default content in `main.tex`
3. **Open** your local `TP06_Report.tex` file
4. **Copy ALL content** from `TP06_Report.tex`
5. **Paste** it into `main.tex` in Overleaf
6. Or click the **"Upload"** button and upload `TP06_Report.tex` directly

### Step 5: Create Images Folder and Upload Images

1. In Overleaf, click the **folder icon** 📁 at the top left (next to "New File")
2. Click **"New Folder"**
3. Name it: **"images"** (lowercase, exactly as shown)
4. Click **"Create"**

5. Click on the **"images"** folder to open it
6. Click the **"Upload"** button ⬆️
7. Select all 8 PNG files you downloaded:
   - feature_distributions.png
   - elbow_silhouette.png
   - kmeans_clusters.png
   - dendrograms.png
   - hierarchical_silhouette.png
   - hierarchical_clusters.png
   - comparison_plot.png
   - boxplots.png
8. Click **"Open"** to upload

### Step 6: Compile the Document

1. Click the green **"Recompile"** button at the top
2. Wait 10-30 seconds for compilation
3. The PDF will appear on the right side! 📄

**Note**: Overleaf automatically compiles. If it doesn't, click "Recompile"

### Step 7: Download Your PDF

1. Once compiled successfully, click the **"Download PDF"** button (download icon) 
2. Save as: **TP06_Report.pdf**
3. **Done!** Your professional report is ready! ✅

## 📋 Checklist

Before compiling, make sure:
- ✅ `main.tex` contains all LaTeX code from `TP06_Report.tex`
- ✅ `images/` folder exists in Overleaf
- ✅ All 8 PNG files are uploaded to the `images/` folder
- ✅ File names match exactly (case-sensitive):
  - feature_distributions.png
  - elbow_silhouette.png
  - kmeans_clusters.png
  - dendrograms.png
  - hierarchical_silhouette.png
  - hierarchical_clusters.png
  - comparison_plot.png
  - boxplots.png

## 🔧 Troubleshooting in Overleaf

### Issue: "File not found: images/xxx.png"
**Solution**: 
- Check that the `images/` folder exists
- Verify all 8 images are uploaded
- Ensure filenames match exactly (case-sensitive)

### Issue: "Compilation timeout"
**Solution**:
- Free Overleaf accounts have 1-minute timeout
- Try compiling again
- Consider upgrading to free Overleaf account (2-minute timeout)

### Issue: "Missing package"
**Solution**:
- Overleaf has most packages pre-installed
- The document uses standard packages, should work fine

### Issue: "PDF shows wrong student name"
**Solution**:
- In `main.tex`, line 53, update: `{\large Name: Chikhaoui Youcef Chihab Eddine\\[0.3cm]}`
- Change to your name
- Click "Recompile"

### Issue: "Table of contents missing page numbers"
**Solution**:
- Click "Recompile" a second time
- LaTeX needs two passes to generate ToC

## 💡 Pro Tips for Overleaf

1. **Auto-compile**: Enable "Auto Compile" in Settings (gear icon) for automatic updates
2. **View Logs**: Click "Logs and output files" to see compilation details
3. **Share Project**: Click "Share" to collaborate with teammates
4. **Download Source**: Click "Menu" → "Source" to download all files as ZIP
5. **History**: Free accounts get 24-hour history - use "History" to revert changes

## 📦 Overleaf Project Structure

Your Overleaf project will look like this:

```
TP06_Clustering_Report/
├── main.tex (your TP06_Report.tex content)
└── images/
    ├── feature_distributions.png
    ├── elbow_silhouette.png
    ├── kmeans_clusters.png
    ├── dendrograms.png
    ├── hierarchical_silhouette.png
    ├── hierarchical_clusters.png
    ├── comparison_plot.png
    └── boxplots.png
```

## 🎯 Quick Summary: Overleaf Workflow

1. **Sign up** at overleaf.com (free)
2. **Create new blank project**
3. **Copy/paste** TP06_Report.tex into main.tex
4. **Create "images" folder** in Overleaf
5. **Upload 8 PNG files** to images folder
6. **Click "Recompile"**
7. **Download PDF** ✅

**Total time**: ~5-10 minutes!

## 💡 Alternative: Download All Images from Colab at Once

If you're using Google Colab, add this cell at the end to download all images as a ZIP:

```python
# Download all images as ZIP
import shutil
import os

# Create images folder if not exists
os.makedirs('images', exist_ok=True)

# Move all PNG files to images folder
import glob
for png_file in glob.glob('*.png'):
    shutil.move(png_file, f'images/{png_file}')

# Create ZIP file
shutil.make_archive('tp06_images', 'zip', 'images')

# Download the ZIP
from google.colab import files
files.download('tp06_images.zip')
```

Then extract the ZIP on your computer and upload all images to Overleaf at once!

## 🎓 Ready to Submit!

Once compiled successfully in Overleaf, you'll have:
- ✅ Professional PDF report with all visualizations
- ✅ Complete analysis answering all TP06 requirements
- ✅ Properly formatted references and citations
- ✅ Table of contents for easy navigation
- ✅ 15+ pages of comprehensive analysis

**No local LaTeX installation needed!** 🚀

## 🌟 Bonus: Local Compilation (Optional)

If you still want to compile locally:

### Install LaTeX:
```bash
sudo apt-get install texlive-full
```

### Compile:
```bash
cd /home/chihab/Documents/cys2CS/AiFondamentalls/tp6
mkdir -p images  # Create images folder
# Copy your 8 PNG files to images/
pdflatex TP06_Report.tex
pdflatex TP06_Report.tex  # Run twice for ToC
```

But **Overleaf is much easier!** �
