import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import heapq


# ==========================================
# 1. 算法逻辑核心 (保持不变)
# ==========================================
class GraphAlgorithms:
    @staticmethod
    def kruskal(nodes, edges, is_directed):
        if is_directed:
            return [], "错误：Kruskal算法（最小生成树）仅适用于【无向图】。\n当前选择的是有向图，请切换模式或算法。"

        parent = {n: n for n in nodes}

        def find(n):
            if parent[n] != n:
                parent[n] = find(parent[n])
            return parent[n]

        def union(n1, n2):
            root1, root2 = find(n1), find(n2)
            if root1 != root2:
                parent[root1] = root2
                return True
            return False

        mst_edges = []
        sorted_edges = sorted(edges, key=lambda x: x[2])
        total_weight = 0
        for u, v, w in sorted_edges:
            if union(u, v):
                mst_edges.append((u, v))
                total_weight += w

        roots = set(find(n) for n in nodes)
        status = "最小生成树(MST)" if len(roots) <= 1 else "最小生成森林(图不连通)"
        return mst_edges, f"{status}完成\n总权重: {total_weight}"

    @staticmethod
    def prim(nodes, edges, is_directed):
        if is_directed:
            return [], "错误：Prim算法（最小生成树）仅适用于【无向图】。"

        if not nodes: return [], "空图"
        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_weighted_edges_from(edges)
        if not nx.is_connected(G):
            return [], "无法执行Prim算法：图不连通。\n请使用Kruskal或补全边。"

        adj = {n: [] for n in nodes}
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        start_node = list(nodes)[0]
        visited = {start_node}
        mst_edges = []
        total_weight = 0
        edges_heap = [(w, start_node, v) for v, w in adj[start_node]]
        heapq.heapify(edges_heap)

        while edges_heap:
            w, u, v = heapq.heappop(edges_heap)
            if v not in visited:
                visited.add(v)
                mst_edges.append((u, v))
                total_weight += w
                for next_node, weight in adj[v]:
                    if next_node not in visited:
                        heapq.heappush(edges_heap, (weight, v, next_node))

        return mst_edges, f"Prim算法完成\n总权重: {total_weight}"

    @staticmethod
    def reverse_delete(nodes, edges, is_directed):
        if is_directed:
            return [], "错误：破圈法（MST）仅适用于【无向图】。"

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_weighted_edges_from(edges)
        if not nx.is_connected(G):
            return [], "无法执行破圈法：图不连通。"

        sorted_edges = sorted(edges, key=lambda x: x[2], reverse=True)
        G_temp = G.copy()

        result_edges = []
        for u, v, w in sorted_edges:
            G_temp.remove_edge(u, v)
            if not nx.is_connected(G_temp):
                G_temp.add_edge(u, v, weight=w)
                result_edges.append((u, v))

        final_edges = [(u, v) for u, v in G_temp.edges()]
        total = sum([d['weight'] for u, v, d in G_temp.edges(data=True)])
        return final_edges, f"破圈法完成\n总权重: {total}"

    @staticmethod
    def dijkstra(nodes, edges, start_node, is_directed):
        for u, v, w in edges:
            if w < 0:
                return [], f"错误：检测到负权边 ({u}->{v}: {w})。\nDijkstra不支持负权。"

        adj = {n: [] for n in nodes}
        for u, v, w in edges:
            adj[u].append((v, w))
            if not is_directed:
                adj[v].append((u, w))

        dist = {n: float('inf') for n in nodes}
        dist[start_node] = 0
        parent = {n: None for n in nodes}
        pq = [(0, start_node)]

        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]: continue
            for v, w in adj[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    parent[v] = u
                    heapq.heappush(pq, (dist[v], v))

        path_edges = []
        for n in nodes:
            if parent[n] is not None:
                path_edges.append((parent[n], n))

        res_str = f"Dijkstra结果 (起点 {start_node}):\n"
        for n in sorted(nodes):
            val = dist[n]
            val_str = "不可达" if val == float('inf') else str(val)
            res_str += f" -> {n} : {val_str}\n"

        return path_edges, res_str


    '''
    nodes	        {'A', 'B', 'C'}
    edges	        三元组列表 (u, v, w) → 从 u 到 v 权重为 w，[('A', 'B', 3.5), ('B', 'C', 2.0)]
    is_directed	    True 有向，False 无向
    '''
    @staticmethod
    def floyd_warshall(nodes, edges, is_directed):
        node_list = sorted(list(nodes))
        idx_map = {n: i for i, n in enumerate(node_list)}#{'A': 0, 'B': 1, 'C': 2}
        n = len(node_list)#节点数

        dist = [[float('inf')] * n for _ in range(n)]# 初始化n×n的距离矩阵，所有值设为无穷大
        for i in range(n): dist[i][i] = 0#对角线上的元素设为0

        for u, v, w in edges:
            if u in idx_map and v in idx_map:
                dist[idx_map[u]][idx_map[v]] = min(dist[idx_map[u]][idx_map[v]], w)# 设置u到v的距离为w，如果有多条边取最小值
                if not is_directed:
                    dist[idx_map[v]][idx_map[u]] = min(dist[idx_map[v]][idx_map[u]], w)# 如果是无向图，同时设置v到u的距离也为w

# 三层循环，经典的Floyd-Warshall算法核心
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] != float('inf') and dist[k][j] != float('inf'):# 只有当i到k和k到j都可达时才更新
                        if dist[i][k] + dist[k][j] < dist[i][j]:# 如果经过k的中转路径更短，更新最短距离
                            dist[i][j] = dist[i][k] + dist[k][j]

        for i in range(n):# 检查负权圈：如果某个节点到自身的距离小于0，说明存在负权圈
            if dist[i][i] < 0:
                return [], "错误：检测到负权圈。\nFloyd算法无法执行。"
#打表
        output_text = "Floyd-Warshall 最短路径矩阵:\n"
        output_text += "(行=起点, 列=终点, 模式=" + ("有向" if is_directed else "无向") + ")\n\n"

        header = "      " + " ".join([f"{node:>6}" for node in node_list])
        output_text += header + "\n" + "-" * len(header) + "\n"
        for i, u in enumerate(node_list):
            row_str = f"{u:>4} |"
            for j in range(n):
                val = dist[i][j]
                val_str = "inf" if val == float('inf') else f"{val:.0f}"
                row_str += f"{val_str:>6} "
            output_text += row_str + "\n"
        return [], output_text

    @staticmethod
    def hungarian(nodes, edges, is_directed):
        if is_directed:
            return [], "错误：匈牙利算法通常处理【无向二分图】匹配问题。\n请切换为无向图模式。"

        G = nx.Graph()
        G.add_nodes_from(nodes)# 添加所有节点
        G.add_weighted_edges_from(edges)# 添加带权重的边

        if not nx.is_bipartite(G):
            return [], "错误：图不是二分图 (存在奇数环)。"

        try:
            '''
            # 使用NetworkX的二分图最大匹配算法
            # 返回一个字典：{节点: 匹配的节点}
            # 例如：{'A': 'X', 'X': 'A', 'B': 'Y', 'Y': 'B'}
            
            程序员: A, B, C
            任务: X, Y, Z
            程序员能做的任务: A能做X,Y；B能做X；C能做Z
            最大匹配结果：A做Y，B做X，C做Z（3个任务都分配了）
            '''
            matching = nx.bipartite.maximum_matching(G)
            match_edges = []# 存储匹配边的列表
            seen = set()# 记录已经处理过的边（避免重复）
            count = 0
            for u, v in matching.items():# 遍历匹配结果中的所有配对
                edge = tuple(sorted((u, v)))# 将边排序后转为元组，确保 (A,X) 和 (X,A) 被视为同一条边# 例如：('A','X') 和 ('X','A') 都会变成 ('A','X')

                if edge not in seen:
                    match_edges.append(edge)
                    seen.add(edge)
                    count += 1
            return match_edges, f"匈牙利算法完成\n最大匹配数: {count}"
        except Exception as e:
            return [], str(e)

    @staticmethod
    def km_algorithm(nodes, edges, is_directed):
        if is_directed:
            return [], "错误：KM算法处理【无向二分图】最大权匹配。\n请切换为无向图模式。"

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_weighted_edges_from(edges)
        if not nx.is_bipartite(G):
            return [], "错误：图不是二分图。"

        try:
            matching = nx.max_weight_matching(G, maxcardinality=True)
            res = list(matching)
            total_w = sum([G[u][v]['weight'] for u, v in res])
            return res, f"KM算法完成\n最大权匹配总重: {total_w}"
        except Exception as e:
            return [], str(e)


# ==========================================
# 2. GUI 主程序
# ==========================================
class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("算法专家 - 图论求解系统 (可视化增强版)")
        self.root.geometry("1100x780")

        self.edges = []
        self.nodes = set()

        # 布局
        left_panel = tk.Frame(root, width=320, bg="#f0f0f0")
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        left_panel.pack_propagate(False)

        right_panel = tk.Frame(root)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- 图类型选择 ---
        tk.Label(left_panel, text="1. 图的类型", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=(5, 0))
        self.graph_type = tk.StringVar(value="undirected")      #默认为无向图

        type_frame = tk.Frame(left_panel, bg="#f0f0f0")
        type_frame.pack(pady=5)
        tk.Radiobutton(type_frame, text="无向图", variable=self.graph_type, value="undirected", bg="#f0f0f0").pack(
            side=tk.LEFT, padx=10)
        tk.Radiobutton(type_frame, text="有向图", variable=self.graph_type, value="directed", bg="#f0f0f0").pack(
            side=tk.LEFT, padx=10)

        # --- 输入 ---
        tk.Label(left_panel, text="2. 输入数据", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=(10, 5))
        tk.Label(left_panel, text="格式: 起点 终点 权重 (严格校验)", bg="#f0f0f0", fg="red").pack()

        self.text_input = tk.Text(left_panel, height=12, width=35, undo=True)
        self.text_input.pack(pady=5)
        self.text_input.insert(tk.END, "A B 3\nA C 4\nB C 2")

        btn_frame = tk.Frame(left_panel, bg="#f0f0f0")
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="校验并绘图", command=self.check_input_only).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="清空", command=lambda: self.text_input.delete("1.0", tk.END)).pack(side=tk.LEFT)

        # --- 算法选择 ---
        tk.Label(left_panel, text="3. 选择算法", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=10)
        self.algo_var = tk.IntVar(value=1)

        algos = [
            (1, "Kruskal算法 (MST)"),
            (2, "Prim算法 (MST)"),
            (3, "破圈法 (MST)"),
            (4, "Dijkstra算法 (最短路)"),
            (5, "Floyd算法 (多源最短路)"),
            (6, "Floyd-Warshall算法"),
            (7, "匈牙利算法 (最大匹配)"),
            (8, "KM算法 (最优匹配)")
        ]
        for val, name in algos:
            tk.Radiobutton(left_panel, text=name, variable=self.algo_var, value=val, bg="#f0f0f0", anchor="w").pack(
                fill=tk.X, padx=10)

        frame_dij = tk.Frame(left_panel, bg="#f0f0f0")
        frame_dij.pack(pady=5)
        tk.Label(frame_dij, text="Dijkstra起点:", bg="#f0f0f0").pack(side=tk.LEFT)
        self.start_node_entry = tk.Entry(frame_dij, width=5)
        self.start_node_entry.pack(side=tk.LEFT, padx=5)
        self.start_node_entry.insert(0, "A")

        tk.Button(left_panel, text="运行算法", command=self.run_algorithm, bg="#D32F2F", fg="white",
                  font=("Arial", 12, "bold"), width=20).pack(pady=15)

        tk.Label(left_panel, text="错误日志:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(anchor="w", padx=5)
        self.log_text = tk.Text(left_panel, height=8, width=40, font=("Consolas", 8), bg="#e0e0e0", fg="red")
        self.log_text.pack(pady=5, padx=5)

        # 绘图
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def log_error(self, msg):
        self.log_text.insert(tk.END, "[Error] " + msg + "\n")
        self.log_text.see(tk.END)

    def parse_input_strict(self):
        content = self.text_input.get("1.0", tk.END).strip()
        self.log_text.delete("1.0", tk.END)

        is_directed = (self.graph_type.get() == "directed")

        nodes = set()
        edges_list = []
        seen_edges = {}

        if not content:
            messagebox.showerror("输入错误", "输入为空！")
            return set(), [], False

        error_found = False
        lines = content.split('\n')

        for i, line in enumerate(lines):
            line_str = line.strip()
            if not line_str: continue

            parts = line_str.split()
            if len(parts) != 3:
                self.log_error(f"行 {i + 1} 格式错误: 需 '起点 终点 权重'")
                error_found = True
                continue

            u, v, w_str = parts[0], parts[1], parts[2]
            try:
                w = float(w_str)
            except ValueError:
                self.log_error(f"行 {i + 1} 权重错误: '{w_str}' 不是数字")
                error_found = True
                continue

            if u == v:
                self.log_error(f"行 {i + 1} 错误: 不允许自环")
                error_found = True
                continue

            if is_directed:
                edge_key = (u, v)
            else:
                edge_key = tuple(sorted((u, v)))

            if edge_key in seen_edges:
                prev_line = seen_edges[edge_key]
                conflict_msg = f"边 {u}->{v}" if is_directed else f"边 {u}-{v}"
                self.log_error(f"行 {i + 1} 冲突: {conflict_msg} 已在行 {prev_line} 定义。")
                error_found = True
                continue

            seen_edges[edge_key] = i + 1
            nodes.add(u)
            nodes.add(v)
            edges_list.append((u, v, w))

        if error_found:
            messagebox.showerror("校验失败", "输入存在错误，请查看日志修正。")
            return set(), [], False

        return nodes, edges_list, True

    def check_input_only(self):
        nodes, edges, valid = self.parse_input_strict()
        if valid:
            type_str = "有向图" if self.graph_type.get() == "directed" else "无向图"
            messagebox.showinfo("校验通过", f"[{type_str}] 校验通过。\n节点: {len(nodes)}\n边: {len(edges)}")
            self.draw_graph(edges, [])

    def draw_graph(self, edges, highlight_edges):
        self.ax.clear()
        is_directed = (self.graph_type.get() == "directed")

        if is_directed:
            G = nx.DiGraph()
        else:
            G = nx.Graph()

        for u, v, w in edges:
            G.add_edge(u, v, weight=w)

        pos = nx.spring_layout(G, seed=42)

        # 节点
        nx.draw_networkx_nodes(G, pos, ax=self.ax, node_color='#90EE90' if not is_directed else '#FFD700',
                               node_size=500, edgecolors='black')
        nx.draw_networkx_labels(G, pos, ax=self.ax, font_weight='bold')

        # 核心修改：如果是由于向图，设置 connectionstyle 为 arc3 (弯曲)，否则为 None (直线)
        # rad=0.1 表示弯曲程度，可以分离双向边
        conn_style = 'arc3, rad=0.1' if is_directed else 'arc3'

        # 边
        nx.draw_networkx_edges(G, pos, ax=self.ax, edge_color='gray',
                               arrows=is_directed, arrowstyle='-|>', arrowsize=20,
                               connectionstyle=conn_style)

        # 权重标签
        edge_labels = {(u, v): f"{d['weight']:.0f}" for u, v, d in G.edges(data=True)}
        # 注意：label_pos 调整是为了稍微避开默认重叠，但有向图弯曲时标签仍可能部分重叠，这是库的限制
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=self.ax, label_pos=0.3)

        if highlight_edges:
            draw_list = []
            if is_directed:
                for u, v in highlight_edges:
                    if G.has_edge(u, v): draw_list.append((u, v))
            else:
                for u, v in highlight_edges:
                    if G.has_edge(u, v):
                        draw_list.append((u, v))
                    elif G.has_edge(v, u):
                        draw_list.append((v, u))

            # 高亮边也必须保持同样的弯曲风格
            nx.draw_networkx_edges(G, pos, edgelist=draw_list, edge_color='red', width=2,
                                   arrows=is_directed, arrowstyle='-|>', arrowsize=20, ax=self.ax,
                                   connectionstyle=conn_style)

        self.canvas.draw()

    def show_matrix(self, content):
        top = tk.Toplevel(self.root)
        top.title("结果矩阵")
        txt = scrolledtext.ScrolledText(top, width=65, height=20, font=("Consolas", 10))
        txt.pack()
        txt.insert(tk.END, content)

    def run_algorithm(self):
        nodes, edges, is_valid = self.parse_input_strict()
        if not is_valid: return

        self.draw_graph(edges, [])

        is_directed = (self.graph_type.get() == "directed")
        choice = self.algo_var.get()
        result_edges = []
        msg = ""

        try:
            if choice == 1:
                result_edges, msg = GraphAlgorithms.kruskal(nodes, edges, is_directed)
            elif choice == 2:
                result_edges, msg = GraphAlgorithms.prim(nodes, edges, is_directed)
            elif choice == 3:
                result_edges, msg = GraphAlgorithms.reverse_delete(nodes, edges, is_directed)
            elif choice == 4:
                start = self.start_node_entry.get().strip()
                if start not in nodes:
                    messagebox.showerror("运行错误", f"起点 {start} 不在图中")
                    return
                result_edges, msg = GraphAlgorithms.dijkstra(nodes, edges, start, is_directed)
            elif choice == 5 or choice == 6:
                result_edges, mat = GraphAlgorithms.floyd_warshall(nodes, edges, is_directed)
                if not mat:
                    messagebox.showerror("算法错误", msg)
                    return
                self.show_matrix(mat)
                msg = "Floyd计算完成 (见弹窗)"
            elif choice == 7:
                result_edges, msg = GraphAlgorithms.hungarian(nodes, edges, is_directed)
            elif choice == 8:
                result_edges, msg = GraphAlgorithms.km_algorithm(nodes, edges, is_directed)

            if not result_edges and ("错误" in msg or "无法执行" in msg):
                messagebox.showerror("算法不兼容", msg)
                self.log_error(msg)
            else:
                messagebox.showinfo("运行成功", msg)
                self.draw_graph(edges, result_edges)

        except Exception as e:
            messagebox.showerror("系统错误", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()