Anchor Finder
A Python system that automatically determines the precise location of a boat's anchor using AIS data and mathematical analysis.
Overview
Traditional anchor alarms require manual estimation of anchor location, which is often imprecise. This project analyzes a boat's natural movement patterns around its anchor to mathematically calculate the exact anchor position using trilateration and Bayesian inference.
How It Works
The system collects real-time vessel position data via the VesselFinder API, processes the boat's movement patterns, and uses geometric analysis to find intersection points of perpendicular lines. Bayesian probability updating determines the most likely anchor location.
Components

anchorfinding.py - Core algorithm implementing trilateration and probability calculations
apiToJson.py - Collects real-time AIS data from VesselFinder API
jsonreader.py - Processes collected data and extracts vessel positions

Results
Successfully tested with 8+ hours of real maritime data. The algorithm accurately predicted anchor locations for vessels showing clear arc movement patterns. Results were validated using geometric verification methods.
Applications
Enhanced anchor alarms with precise boundaries, early anchor dragging detection, fleet monitoring using AIS data, and improved maritime safety in anchorages.
Technical Stack
Python, NumPy, Matplotlib, real-time API integration, geospatial analysis, Bayesian statistics.
