# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "anywidget",
# ]
# ///

import marimo

__generated_with = "0.20.2"
app = marimo.App(width="columns")

with app.setup:
    import marimo as mo


@app.cell
def _():
    import anywidget
    import traitlets

    return anywidget, traitlets


@app.cell(hide_code=True)
def _(anywidget, traitlets):
    class DLAWidget(anywidget.AnyWidget):
        _esm = """
        function render({ model, el }) {
          // Canvas setup
          const canvas = document.createElement("canvas");
          const size = 600;
          canvas.width = size;
          canvas.height = size;
          canvas.style.borderRadius = "8px";
          canvas.style.boxShadow = "0 4px 6px rgba(0, 0, 0, 0.1)";

          const ctx = canvas.getContext("2d");
          const center = size / 2;
          const gridSize = 300; // Grid spans -150 to 150
          const scale = size / gridSize;

          // DLA state
          let cluster = new Set();
          let clusterRadius = 1;
          const spawnBuffer = 5;
          const killRadiusMultiplier = 2.5;

          // Add seed particle at origin
          cluster.add("0,0");

          // Convert grid coords to canvas coords
          function toCanvas(x, y) {
            return {
              x: center + x * scale,
              y: center + y * scale
            };
          }

          // Check if a position is occupied
          function isOccupied(x, y) {
            return cluster.has(`${x},${y}`);
          }

          // Check if a position has an occupied neighbor
          function hasNeighbor(x, y) {
            const dirs = [[-1,0], [1,0], [0,-1], [0,1], [-1,-1], [-1,1], [1,-1], [1,1]];
            for (let [dx, dy] of dirs) {
              if (cluster.has(`${x+dx},${y+dy}`)) return true;
            }
            return false;
          }

          // Random walk one particle
          function walkParticle() {
            // Spawn on circle outside cluster
            const spawnRadius = clusterRadius + spawnBuffer;
            const angle = Math.random() * Math.PI * 2;
            let x = Math.round(Math.cos(angle) * spawnRadius);
            let y = Math.round(Math.sin(angle) * spawnRadius);

            const killRadius = clusterRadius + spawnBuffer * 3;

            // Random walk until stick or escape
            for (let steps = 0; steps < 50000; steps++) {
              // Random step (8 directions)
              const dir = Math.floor(Math.random() * 8);
              const moves = [[-1,0], [1,0], [0,-1], [0,1], [-1,-1], [-1,1], [1,-1], [1,1]];
              const newX = x + moves[dir][0];
              const newY = y + moves[dir][1];

              // Don't move into occupied space
              if (isOccupied(newX, newY)) {
                // Can't move there, but we're stuck here!
                cluster.add(`${x},${y}`);
                const dist = Math.sqrt(x*x + y*y);
                if (dist > clusterRadius) clusterRadius = dist;
                return true;
              }

              // Move to new position
              x = newX;
              y = newY;

              // Check if now touching cluster
              if (hasNeighbor(x, y)) {
                cluster.add(`${x},${y}`);
                const dist = Math.sqrt(x*x + y*y);
                if (dist > clusterRadius) clusterRadius = dist;
                return true; // Stuck!
              }

              // Kill if too far
              const currentDist = Math.sqrt(x*x + y*y);
              if (currentDist > killRadius) return false;
            }
            return false;
          }

          // Draw the cluster
          function draw() {
            // Clear with background
            const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            ctx.fillStyle = isDark ? "#1a1a1a" : "#ffffff";
            ctx.fillRect(0, 0, size, size);

            // Draw particles
            const particleSize = Math.max(1, scale * 0.8);

            for (let key of cluster) {
              const [x, y] = key.split(',').map(Number);
              const pos = toCanvas(x, y);

              // Color based on distance from center (creates gradient effect)
              const dist = Math.sqrt(x*x + y*y);
              const normalizedDist = dist / clusterRadius;

              // Beautiful gradient: purple to cyan to pink
              const hue = 270 + normalizedDist * 90; // 270 (purple) to 360 (pink/magenta)
              const saturation = 70 + normalizedDist * 20;
              const lightness = isDark ? 50 + normalizedDist * 20 : 40 + normalizedDist * 20;

              ctx.fillStyle = `hsl(${hue}, ${saturation}%, ${lightness}%)`;
              ctx.fillRect(
                pos.x - particleSize/2,
                pos.y - particleSize/2,
                particleSize,
                particleSize
              );
            }

            // Update particle count
            model.set("particle_count", cluster.size);
            model.save_changes();
          }

          // Animation loop
          let running = false;
          let animationId = null;

          function animate() {
            if (!running) return;

            // Add multiple particles per frame for speed
            // Try more particles when cluster is small
            const particlesPerFrame = cluster.size < 100 ? 10 : 5;
            for (let i = 0; i < particlesPerFrame; i++) {
              walkParticle();
            }

            draw();

            // Stop if cluster gets too large
            if (cluster.size < 3000) {
              animationId = requestAnimationFrame(animate);
            } else {
              running = false;
              model.set("is_running", false);
              model.save_changes();
            }
          }

          // Control panel
          const controls = document.createElement("div");
          controls.className = "controls";

          const startBtn = document.createElement("button");
          startBtn.textContent = "Start Growth";
          startBtn.className = "btn";
          startBtn.addEventListener("click", () => {
            running = !running;
            startBtn.textContent = running ? "Pause" : "Resume Growth";
            if (running) animate();
          });

          const resetBtn = document.createElement("button");
          resetBtn.textContent = "Reset";
          resetBtn.className = "btn btn-secondary";
          resetBtn.addEventListener("click", () => {
            running = false;
            if (animationId) cancelAnimationFrame(animationId);
            cluster.clear();
            cluster.add("0,0");
            clusterRadius = 1;
            startBtn.textContent = "Start Growth";
            draw();
          });

          const info = document.createElement("div");
          info.className = "info";
          info.textContent = `Particles: ${cluster.size}`;

          controls.appendChild(startBtn);
          controls.appendChild(resetBtn);
          controls.appendChild(info);

          // Update info display
          model.on("change:particle_count", () => {
            info.textContent = `Particles: ${model.get("particle_count")}`;
          });

          // Initial draw
          draw();

          // Append to element
          el.appendChild(canvas);
          el.appendChild(controls);
        }
        export default { render };
        """

        _css = """
        .controls {
          display: flex;
          gap: 12px;
          margin-top: 16px;
          align-items: center;
          flex-wrap: wrap;
        }

        .btn {
          padding: 10px 24px;
          min-width: 140px;
          font-size: 14px;
          font-weight: 500;
          border: 1px solid #d1d5db;
          border-radius: 6px;
          cursor: pointer;
          transition: all 0.15s ease;
          background: #ffffff;
          color: #374151;
        }

        .btn:hover {
          border-color: #9ca3af;
          background: #f9fafb;
        }

        .btn:active {
          background: #f3f4f6;
        }

        .btn-secondary {
          border-color: #d1d5db;
        }

        .info {
          font-size: 14px;
          font-weight: 500;
          color: #1f2937;
          padding: 10px 16px;
          background: #f3f4f6;
          border: 1px solid #e5e7eb;
          border-radius: 6px;
        }

        canvas {
          display: block;
          max-width: 100%;
          height: auto;
        }

        @media (prefers-color-scheme: dark) {
          .btn {
            background: #1f2937;
            color: #f9fafb;
            border-color: #4b5563;
          }

          .btn:hover {
            background: #374151;
            border-color: #6b7280;
          }

          .btn:active {
            background: #4b5563;
          }

          .info {
            color: #f9fafb;
            background: #1f2937;
            border-color: #4b5563;
          }

          canvas {
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3) !important;
          }
        }
        """

        particle_count = traitlets.Int(1).tag(sync=True)
        is_running = traitlets.Bool(False).tag(sync=True)

    return (DLAWidget,)


@app.cell
def _():
    mo.md("""
    # Diffusion-limited aggregation (DLA)

    Diffusion-Limited aggregation is a simple model for how branching, fractal patterns form when particles move randomly and stick together on contact. It appears in nature whenever growth is limited by diffusion... this process helps shape lightning paths, mineral dendrites, soot, and many types of crystal growth.

    This simulation shows how such geometry can emergy from nothing more than random motion and sticking -- how complex structure can arise from very simple rules.
    """)
    return


@app.cell
def _(DLAWidget):
    dla_widget = mo.ui.anywidget(DLAWidget())
    dla_widget
    return (dla_widget,)


@app.cell(hide_code=True)
def _(dla_widget):
    mo.md(f"""
    **Current State:**
    - Particles in cluster: {dla_widget.value.get("particle_count", 1)}
    - Running: {dla_widget.value.get("is_running", False)}
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## A simple model

    Imagine tiny particles drifting randomly through space. When one touches a growing cluster, it sticks and becomes part of the structure. Over time, this produces branching shapes with long arms and empty gaps—patterns that are “fractal,” meaning they look similar at different scales. The key idea is that growth is limited by diffusion: particles reach the outer tips of the cluster more easily than the interior, so those tips grow faster and keep extending outward.


    ## Why did I simulate this?

    DLA is one of the simplest examples of how complex structures can arise without a blueprint. With only randomness and a basic sticking rule, you get patterns that resemble coral, trees, or river networks. This is satisfying to watch.

    I was first introduced to DLA in high school -- or perhaps it was early college days -- when I was reading James Gleick's "Chaos". My friend Arian and I wrote simple programs to recreate this algorithm (and several others, too). Through the years we've tried variations and experimented with user-controlled knobs, to make the visualization more compelling.

    Now it's turned into sort-of "hello world" code, written in many languages, platforms, styles.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
