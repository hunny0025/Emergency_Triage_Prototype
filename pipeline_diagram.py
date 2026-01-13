import plotly.graph_objects as go

fig = go.Figure(go.Sankey(
    node = dict(
        pad = 15,
        thickness = 20,
        line = dict(color = "black", width = 0.5),
        label = ["Voice Input", "STT", "LLM", "Rules", "Output"],
        color = ["#4F46E5", "#7C3AED", "#EC4899", "#F59E0B", "#10B981"]
    ),
    link = dict(
        source = [0, 1, 2, 3],
        target = [1, 2, 3, 4],
        value = [1, 1, 1, 1]
    )
))