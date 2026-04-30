# Dijkstra Routing Simulator

This is a Python Streamlit simulator for Dijkstra's algorithm and link-state routing.

## Features

- Visual weighted network graph
- Shortest path view
- Shortest-path tree view
- Step-by-step Dijkstra view
- Link failure and restoration
- Forwarding table

## How to run

Open PowerShell inside this folder and run:

```powershell
pip install -r requirements.txt
streamlit run app.py
```

If Streamlit is not recognized, run:

```powershell
python -m streamlit run app.py
```

## Demo explanation

This simulator represents a network as a weighted graph. Each router is a node, each link is an edge, and the number on each link is the cost. Dijkstra's algorithm finds the lowest-cost paths from the source router to every other router. The forwarding table shows the next hop for each destination. If a link is cut, the graph changes and the algorithm reruns, similar to how link-state routing protocols such as OSPF update routes after LSAs are flooded.
