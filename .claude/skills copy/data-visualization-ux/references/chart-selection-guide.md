# Chart Type Selection Guide

## Decision Tree

```
START: What are you trying to show?
├─ COMPARISON (compare values across categories)
│  ├─ Few categories (2-5)?
│  │  ├─ Simple values → Bar Chart
│  │  ├─ Part-to-whole → Pie Chart (use sparingly)
│  │  └─ Part-to-whole, animated → Donut Chart
│  └─ Many categories (6+)?
│     ├─ Horizontal space available → Horizontal Bar Chart
│     └─ Vertical space available → Vertical Bar Chart
│
├─ TREND (show change over time)
│  ├─ Single series → Line Chart
│  ├─ Multiple series (2-3) → Multiple Line Chart
│  ├─ Multiple series (4+) → Area Chart (stacked)
│  ├─ Cumulative change → Stacked Area Chart
│  └─ Rates of change → Slope Chart
│
├─ DISTRIBUTION (show how data is spread)
│  ├─ Single variable → Histogram
│  ├─ Single variable, detailed → Box Plot
│  ├─ Multiple variables → Violin Plot
│  └─ Large sample, density → Density Plot
│
├─ RELATIONSHIP (show correlation/causation)
│  ├─ Two numeric variables → Scatter Plot
│  ├─ Trend + relationship → Scatter with Trendline
│  └─ Multiple variables → Bubble Chart
│
├─ COMPOSITION (show parts of a whole)
│  ├─ Static breakdown → Pie Chart
│  ├─ Over time → Stacked Bar Chart
│  ├─ Over time, percentages → 100% Stacked Bar
│  └─ Hierarchy of parts → Treemap
│
└─ DENSITY/PATTERNS (show concentration/hotspots)
   ├─ Geographic data → Heatmap (geographic)
   ├─ Matrix data → Heatmap (rectangular)
   ├─ Time series with intensity → Heatmap (calendar)
   └─ Spatial clustering → Scatter Heatmap
```

## Chart Types: When to Use

### Bar Chart
**What it shows**: Comparison of values across categories
**When to use**:
- Comparing 2-10 categories
- When absolute values are important
- Part-to-whole comparisons (stacked bars)
**When NOT to use**:
- More than 10 categories (use horizontal bars)
- Trends over time (use line chart)

**Example data**:
```
Platform | Users
---------|------
macOS    | 45000
Linux    | 28000
Web      | 52000
```

### Line Chart
**What it shows**: Trends and changes over time
**When to use**:
- Time series data (hourly, daily, monthly)
- Multiple series to show comparison over time
- Rate of change is important
**When NOT to use**:
- Single point comparisons (use bar)
- More than 5-7 lines (becomes cluttered)

**Example data**:
```
Date       | Scenes | Characters
-----------|--------|------------
2024-01-01 | 12     | 8
2024-01-02 | 15     | 10
2024-01-03 | 18     | 12
```

### Scatter Plot
**What it shows**: Relationship between two continuous variables
**When to use**:
- Showing correlation or causation
- Outlier detection
- Density of data points
**When NOT to use**:
- Categorical data (use bar chart)
- Single variable distribution (use histogram)

**Example data**:
```
Project          | Scenes | Analysis_Time_Hours
-----------------|--------|---------------------
Screenplay_A     | 25     | 4.2
Screenplay_B     | 15     | 2.8
Screenplay_C     | 42     | 6.1
```

### Heatmap
**What it shows**: Patterns across two dimensions, intensity via color
**When to use**:
- Matrix of data (e.g., user activity by day/hour)
- Geographic data with intensity
- Correlation matrices
**When NOT to use**:
- Few data points (use table)
- Precise value reading needed (values too small)

**Example data**:
```
       Mon  Tue  Wed  Thu  Fri
09:00  12   15   10   18   22
12:00  45   52   48   61   58
15:00  38   42   40   55   49
```

### Pie/Donut Chart
**What it shows**: Composition (part-to-whole)
**When to use**:
- 2-3 categories with clear dominant/minority
- Showing percentage breakdown
- Aesthetic/dashboard purposes
**When NOT to use**:
- More than 4 segments (viewers struggle with angles)
- Precise percentage comparison needed
- More than one pie chart in dashboard

**Example data**:
```
Analysis_Type | Percentage
--------------|----------
Scene_Analysis| 45%
Character     | 35%
Location      | 20%
```

### Area Chart
**What it shows**: Composition over time or stacked trends
**When to use**:
- Multiple series over time where composition matters
- Cumulative trends
- Part-to-whole over time
**When NOT to use**:
- More than 3-4 series (hard to read stacked areas)
- Comparing individual series values (use multiple lines)

**Example data**:
```
Date       | AI_Analysis | Manual_Review | Pending
-----------|-------------|---------------|---------
2024-01-01 | 50          | 30            | 20
2024-01-02 | 65          | 25            | 10
2024-01-03 | 80          | 15            | 5
```

### Histogram
**What it shows**: Distribution of a single variable
**When to use**:
- Understanding data spread/density
- Identifying skewness or modality
- Finding outliers
**When NOT to use**:
- Categorical data (use bar chart)
- Small sample sizes (<30 points)

**Example data**:
```
Word_Count_Ranges
0-100
100-200
200-300
300-400
```

### Box Plot
**What it shows**: Statistical distribution (quartiles, median, outliers)
**When to use**:
- Comparing distributions across groups
- Identifying outliers
- Statistical summary needed
**When NOT to use**:
- Audiences unfamiliar with quartile concept
- Individual data point values needed

### Treemap
**What it shows**: Hierarchical part-to-whole composition
**When to use**:
- Showing hierarchy of parts (nested categories)
- Space-filled composition view
- Comparing many items' relative sizes
**When NOT to use**:
- Only 2-3 categories (use pie)
- Precise value comparison (hard to judge rectangle areas)

## Khaos Machine Examples

### Screenplay Analysis Dashboard

**Chart 1: Scene Status Distribution**
- **Data**: Analyzed | Pending | Failed
- **Type**: Stacked bar chart (horizontal)
- **Why**: Easy comparison of status across multiple projects

**Chart 2: Analysis Progress Over Time**
- **Data**: Scenes, Characters, Locations by date
- **Type**: Multiple line chart
- **Why**: Shows trend of how much content has been analyzed

**Chart 3: Scene Mood Distribution**
- **Data**: Happy, Sad, Tense, Neutral counts
- **Type**: Pie chart
- **Why**: Shows composition; 4 categories is manageable

**Chart 4: Character Appearances**
- **Data**: Character name vs scene count
- **Type**: Horizontal bar chart (sorted by count)
- **Why**: Easy to read list of characters ranked by appearances

**Chart 5: Emotional Arc Over Story**
- **Data**: Mood/intensity over scene sequence
- **Type**: Area chart with color zones
- **Why**: Shows flow of emotional intensity through screenplay

**Chart 6: Analysis Time vs Screenplay Complexity**
- **Data**: Word count vs analysis hours (by screenplay)
- **Type**: Scatter plot with bubble size = scene count
- **Why**: Reveals relationship between complexity and analysis time

## Responsiveness Considerations

### Mobile (< 600px)
- Simplify complex charts (reduce data points shown)
- Stack charts vertically instead of grid
- Use wider bars (easier to tap)
- Move legend below chart
- Larger font sizes (14px minimum)
- Consider switching to table view for dense data

### Tablet (600px - 1024px)
- 2 columns max for dashboard grid
- Slightly reduced data point counts
- Legend can be on side for simple charts
- Touch-friendly interaction areas (44px minimum)

### Desktop (> 1024px)
- Full data detail
- Optimal aspect ratios (16:9 or 4:3)
- Legends positioned for balance
- Hover tooltips available
- Zoom/pan available for dense charts
