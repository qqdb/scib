from .common import *
import numpy as np
import scanpy as sc


@pytest.fixture(scope="module")
def adata_factory():
    def adata_factory_(pca=False, n_top_genes=None, neighbors=False):
        adata = sc.datasets.paul15()
        adata.obs['celltype'] = adata.obs['paul15_clusters']
        np.random.seed(42)
        adata.obs['batch'] = np.random.randint(1, 5, adata.n_obs)
        adata.obs['batch'] = adata.obs['batch'].astype(str)
        adata.obs['batch'] = adata.obs['batch'].astype("category")
        adata.layers['counts'] = adata.X
        scIB.preprocessing.reduce_data(
            adata,
            pca=pca,
            n_top_genes=n_top_genes,
            umap=False,
            neighbors=neighbors
        )
        return adata
    return adata_factory_


@pytest.fixture(scope="module")
def adata_embed(adata_factory):
    adata = adata_factory(pca=True, n_top_genes=2000)
    mtx = sc.tl.pca(adata, copy=True).obsm['X_pca']
    adata.obsm['X_emb'] = mtx
    return adata
