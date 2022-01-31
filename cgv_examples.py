from dash import html, Dash
from jbrowse_jupyter import create, create_component

app = Dash(__name__)
base = "https://jbrowse.org/genomes/hg19/fasta/"
base2 = "https://s3.amazonaws.com/jbrowse.org/genomes/hg19/"
file_name = 'hs37d5.HG002-SequelII-CCS.bnd-only.sv.vcf.gz'
my_assembly = {
    "name": "hg19",
    "aliases": ["GRCh37"],
    "sequence": {
        "type": "ReferenceSequenceTrack",
        "trackId": "Pd8Wh30ei9R",
        "adapter": {
            "type": "BgzipFastaAdapter",
            "fastaLocation": {
                "uri": f'{base}hg19.fa.gz',
                "locationType": 'UriLocation',
            },
            "faiLocation": {
                "uri": f'{base}hg19.fa.gz.fai',
                "locationType": 'UriLocation',
            },
            "gziLocation": {
                "uri": f'{base}fasta/hg19.fa.gz.gzi',
                "locationType": 'UriLocation',
            },
        },
    },
    "refNameAliases": {
        "adapter": {
            "type": "RefNameAliasAdapter",
            "location": {
                "uri": f'{base2}hg19_aliases.txt',
                "locationType": 'UriLocation',
            },
        },
    },
}
my_tracks = [
    {
        "type": "VariantTrack",
        "trackId": "pacbio_sv_vcf",
        "name": "HG002 Pacbio SV (VCF)",
        "assemblyNames": ["hg19"],
        "category": ["GIAB"],
        "adapter": {
            "type": "VcfTabixAdapter",
            "vcfGzLocation": {
                "uri": f'{base2}pacbio/{file_name}',
                "locationType": 'UriLocation',
            },
            "index": {
                "location": {
                    "uri": f'{base2}pacbio/{file_name}.tbi',
                    "locationType": 'UriLocation',
                },
            },
        },
    },
]
my_default_session = {
    "name": "My session",
    "view": {
        "id": "circularView",
        "type": "CircularView",
        "bpPerPx": 5000000,
        "tracks": [{
            "id": 'uPdLKHik1',
            "type": 'VariantTrack',
            "configuration": 'pacbio_sv_vcf',
            "displays": [
                {
                    "id": 'v9QVAR3oaB',
                    "type": 'ChordVariantDisplay',
                    "configuration": 'pacbio_sv_vcf-ChordVariantDisplay',
                },
            ],
        }],
    },
}
# create config and pass additional params
config = {
    "assembly": my_assembly,
    "defaultSession": my_default_session,
    "tracks": my_tracks
}
cgv_with_conf = create(view_type="CGV", conf=config)


cgv_with_api = create(view_type="CGV")
cgv_with_api.set_assembly(f'{base}hg19.fa.gz', aliases=["GRCh37"])
cgv_with_api.add_track(f'{base2}pacbio/{file_name}', track_id="variantTest")
cgv_with_api.set_default_session(["variantTest"], False)
cgv_with_api.set_theme("#311b92", "#0097a7", "#f57c00", "#d50000")
# create a dash component
component = create_component(cgv_with_conf.get_config(), dash_comp="CGV")
cvg_default = create("CGV", genome="hg19").get_config()
component2 = create_component(cvg_default, id="test2", dash_comp="CGV")
cgv3 = cgv_with_api.get_config()
component3 = create_component(cgv3, id="test3", dash_comp="CGV")
# launch the component
# 3 different ways to configure, 3 identical components
app.layout = html.Div(
    [component, component2, component3],
    id='test'
)

if __name__ == "__main__":
    app.run_server(port=3003, debug=True)
