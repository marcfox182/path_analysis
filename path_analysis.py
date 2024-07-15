import pandas as pd
import networkx as nx
from collections import defaultdict, Counter
import csv
from urllib.parse import urlparse
import sys
sys.stderr = open('error_log.txt', 'w')


def load_data(csv_file):
    return pd.read_csv(csv_file)

def load_gsc_data(gsc_csv_file):
    return pd.read_csv(gsc_csv_file)

def build_graph(df):
    G = nx.DiGraph()
    header_links, footer_links = set(), set()
    anchor_texts = defaultdict(Counter)
    for _, row in df.iterrows():
        from_url, to_url = row['From'], row['To']
        anchor_text = row['Anchor Text'] if pd.notna(row['Anchor Text']) and row['Anchor Text'].strip() else "Sem Texto Âncora"
        G.add_edge(from_url, to_url, anchor=anchor_text)
        if "header" in str(row.get('Link Path', '')):
            header_links.add(to_url)
        if "footer" in str(row.get('Link Path', '')):
            footer_links.add(to_url)
        anchor_texts[to_url][anchor_text] += 1
    return G, anchor_texts, header_links, footer_links

def find_gsc_metrics(gsc_df, url):
    filtered_data = gsc_df[gsc_df['Páginas principais'] == url]
    if not filtered_data.empty:
        data = filtered_data.iloc[0]
        return {
            'Cliques': data['Cliques'],
            'Impressões': data['Impressões'],
            'CTR': data['CTR'],
            'Posição': data['Posição'],
            'Ranking': gsc_df[gsc_df['Cliques'] >= data['Cliques']].shape[0]
        }
    else:
        return {
            'Cliques': 0,
            'Impressões': 0,
            'CTR': 0.0,
            'Posição': 0,
            'Ranking': 0
        }

def find_paths_and_analyze(G, start_url, target_url, header_links, footer_links, max_depth, gsc_df):
    all_paths = list(nx.all_simple_paths(G, source=start_url, target=target_url, cutoff=max_depth))
    if not all_paths:
        return None
    shortest_path = min(all_paths, key=len)
    path_anchors = [G.edges[u, v]['anchor'] for u, v in zip(shortest_path[:-1], shortest_path[1:])]
    depth_counts = Counter(len(path) - 1 for path in all_paths)
    start_metrics = find_gsc_metrics(gsc_df, start_url)
    target_metrics = find_gsc_metrics(gsc_df, target_url)
    return {
        'shortest_path': shortest_path,
        'path_anchors': path_anchors,
        'depth_counts': depth_counts,  # Make sure to include this
        'start_metrics': start_metrics,
        'target_metrics': target_metrics,
        'direct_from_home': 'Sim' if target_url in G[start_url] else 'Não',
        'in_header': 'Sim' if target_url in header_links else 'Não',
        'in_footer': 'Sim' if target_url in footer_links else 'Não'
    }

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Caminho de URL", "Caminho de Âncoras"])
        for path, anchors in data:
            writer.writerow(["> ".join(path), "> ".join(anchors)])

def generate_html_report(seo_data, filename, anchor_texts, max_clicks):
    target_url = seo_data['shortest_path'][-1]
    domain = urlparse(target_url).netloc.replace(".", "-").replace("/", "-")
    specific_anchor_texts = anchor_texts

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"""<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEO: Análise de Rota do Usuário {domain}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ font-family: Arial, sans-serif; }}
        .header {{ background-color: #f8f9fa; padding: 20px 0; border-bottom: 2px solid #dee2e6; }}
        .card {{ margin-top: 20px; }}
        .card-header {{ background-color: #007bff; color: #ffffff; }}
        footer {{ background-color: #f8f9fa; padding: 20px 0; border-top: 2px solid #dee2e6; color: #6c757d; }}
        .anchor-count {{ background-color: #f0f0f0; padding: 10px; border-radius: 5px; margin-bottom: 10px; }}
        .summary {{ background-color: #e9ecef; padding: 15px; border-radius: 8px; margin-top: 20px; }}
        .important {{ color: #dc3545; }}
    </style>
</head>
<body>
    <div class="container mt-3">
        <header class="text-center header">
            <h1>SEO: Análise de Rota do Usuário {domain}</h1>
        </header>

        <div class="summary">
            <p>Origem: <a href="{seo_data['shortest_path'][0]}">{seo_data['shortest_path'][0]}</a> (cliques: {seo_data['start_metrics']['Cliques']} | impressões: {seo_data['start_metrics']['Impressões']} | posição média: {seo_data['start_metrics']['Posição']} | ranking de tráfego: {seo_data['start_metrics']['Ranking']}°)</p>
            <p>Destino: <a href="{target_url}">{target_url}</a> (cliques: {seo_data['target_metrics']['Cliques']} | impressões: {seo_data['target_metrics']['Impressões']} | posição média: {seo_data['target_metrics']['Posição']} | ranking de tráfego: {seo_data['target_metrics']['Ranking']}°)</p>
            <p>Arquivo de entrada: <span class="important">inlinks.csv</span></p>
            <p>Profundidade máxima: <span class="important">{max_clicks}</span></p>
            <p>Link direto da home: <span class="important">{seo_data['direct_from_home']}</span></p>
            <p>Link no Header: <span class="important">{seo_data['in_header']}</span></p>
            <p>Link no Footer: <span class="important">{seo_data['in_footer']}</span></p>
        </div>

        <div class="card">
            <div class="card-header">Distribuição da Profundidade dos Links</div>
            <div class="card-body">
                {"".join(f"<p>Profundidade {depth}: <span class='important'>{count} link(s)</span></p>" for depth, count in sorted(seo_data['depth_counts'].items()))}
            </div>
        </div>

        <div class="card">
            <div class="card-header">Textos de Âncora Utilizados</div>
            <div class="card-body">
                <div class="row">
                    {"".join(f'<div class="col-md-4 anchor-count">{anchor}: <span class="important">{count} vezes</span></div>' for anchor, count in sorted(specific_anchor_texts.items(), key=lambda item: item[1], reverse=True))}
                </div>
            </div>
        </div>

        <footer class="text-center">
            <p>UpSEO Academy - Venha aprender SEO de verdade</p>
        </footer>
    </div>
</body>
</html>
""")


def save_enhanced_paths_to_csv(G, start_url, target_url, max_depth, gsc_df, anchor_texts, header_links, footer_links,
                               filename):
    all_paths = list(nx.all_simple_edge_paths(G, source=start_url, target=target_url, cutoff=max_depth))
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Caminho Completo", "Profundidade", "Textos de Âncora", "Quantidade de Links", "Link Position",
                         "Métricas de SEO (Cliques, Impressões, CTR, Posição)"])

        for path in all_paths:
            path_urls = [start_url] + [v for _, v in path]
            anchors = [G[u][v]['anchor'] for u, v in path]
            links_count = [len(list(G.successors(u))) for u, v in path]
            link_position = ["Header" if v in header_links else "Footer" if v in footer_links else "Body" for _, v in
                             path]
            seo_metrics = [
                f"{find_gsc_metrics(gsc_df, u)['Cliques']}, {find_gsc_metrics(gsc_df, u)['Impressões']}, {find_gsc_metrics(gsc_df, u)['CTR']}, {find_gsc_metrics(gsc_df, u)['Posição']}"
                for u in path_urls]

            writer.writerow([
                "> ".join(path_urls),
                len(path),
                "> ".join(anchors),
                ", ".join(map(str, links_count)),
                ", ".join(link_position),
                "; ".join(seo_metrics)
            ])


def extended_interactive_search():
    inlinks_csv = input("Digite o nome do arquivo Inlinks CSV: ")
    gsc_csv = input("Digite o nome de Páginas do GSC em CSV: ")
    target_url = input("Digite o URL de Destino: ")
    start_url = input("Digite o URL Inicial: ")
    max_clicks = int(input("Digite o número máximo de cliques que deseja listar (profundidade máxima): "))

    df = load_data(inlinks_csv)
    gsc_df = load_gsc_data(gsc_csv)
    G, anchor_texts, header_links, footer_links = build_graph(df)

    domain = urlparse(start_url).netloc.replace(".", "-").replace("/", "-")
    all_paths_filename = f"{domain}_enhanced_paths.csv"
    html_filename = f"{domain}.html"

    seo_data = find_paths_and_analyze(G, start_url, target_url, header_links, footer_links, max_clicks, gsc_df)
    if seo_data:
        save_enhanced_paths_to_csv(G, start_url, target_url, max_clicks, gsc_df, anchor_texts, header_links, footer_links, all_paths_filename)
        generate_html_report(seo_data, html_filename, anchor_texts[target_url], max_clicks)
        print(f"Todos os caminhos enriquecidos foram salvos em {all_paths_filename}")
        print(f"Relatório HTML gerado e salvo como {html_filename}")
    else:
        print("Não foram encontrados caminhos do URL inicial para o URL de destino dentro da profundidade máxima especificada.")

if __name__ == "__main__":
    extended_interactive_search()