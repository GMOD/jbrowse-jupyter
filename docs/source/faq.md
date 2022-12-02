## FAQ
* What file types are supported?
    - We currently support:
        * bam
        * big wig
        * big bed
        * cram
        * fasta indexed
        * fasta gzipped
        * gff3 tabix
        * two bit
        * vcf
        * vcf gzipped

* What track types are supported?
    - We currently support:
        * [AlignmentsTrack](https://jbrowse.org/jb2/docs/user_guide/#alignments-tracks)
        * [QuantitativeTrack](https://jbrowse.org/jb2/docs/user_guide/#bigwig-tracks)
        * [VariantTrack](https://jbrowse.org/jb2/docs/user_guide/#variant-tracks)
        * [ReferenceSequenceTrack](https://jbrowse.org/jb2/docs/user_guide/#sequence-track)
        * Feature Tracks

    For the circular genome view (CGV), we only support variant tracks. Check out [track types](https://jbrowse.org/jb2/docs/user_guide/#sequence-track) docs for more information.
* What views do you currently support?
    - We currently support JBrowse's Linear Genome View and Circular Genome View. We hope to support more in the future.
* How do I configure text searching?
    - In order to configure text searching in your Linear Genome View, you must first create a text index. Follow the steps found [here](https://jbrowse.org/jb2/docs/quickstart_cli/#indexing-feature-names-for-searching). Then you must create and add a text search adapter to your config. 
* How do I configure tracks to show up on first render?
    - You can set a specific track/tracks to show up when the component first renders, and you can do this via the default session. You can set the default session via the JBrowseConfig API. `set_default_session`
* How do I set a custom color theme palette to fit with my application?
    - You can customize the color palette of the component through the use of `set_theme` function from the JBrowseConfig API. Below is an image of an LGV with a custom color palette. 
![Custom Palette](https://github.com/GMOD/jbrowse-jupyter/raw/main/images/custom_palette.png)

* Can I use local files/my own data?
    - Yes, there are a couple of ways in which you can configure and use your own data from your local environment in jbrowse views. 
        1. Make use of the jupyter notebook/lab server. Intended for those running their notebooks with jupyter lab or jupyter notebook.
        2. Launch your own http server with CORS which will enable you to use local files. You can run our serve.py to launch our dev server. 
    (Checkout our local_support.ipynb for tutorials on how to use your own data)

> **Note**: These solutions are recommended for your development environments and not supported in production.
* I am running a colab notebook/binder notebook and wish to use my local data, how can I do this? 
    - You can run JBrowse dev server to serve local files to use in your JBrowse views. More information on the dev server can be found in the local file support section of this readme.
