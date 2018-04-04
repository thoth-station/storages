"""Various utilities and helper methods for the Graph database."""

from aiogremlin.process.graph_traversal import AsyncGraphTraversalSource
from gremlin_python.process.graph_traversal import addV
from gremlin_python.process.graph_traversal import unfold

from .models_base import VertexBase
from .models_base import EdgeBase


async def get_or_create_vertex(g: AsyncGraphTraversalSource, vertex: VertexBase) -> tuple:
    """Create a vertex if not existed before, if the given vertex already exists, get tis id."""
    query = g.V()
    creation = addV(vertex.__label__)

    for key, value in vertex.to_dict().items():
        if value is not None:
            query = query.has(key, value)
            creation = creation.property(key, value)
        else:
            query = query.hasNot(key)

    result = await query.fold().coalesce(
            unfold().id().as_('id').constant(True).as_('existed').select('id', 'existed'),
            creation.id().as_('id').constant(False).as_('existed').select('id', 'existed')
        ).next()

    # Assign to instance so instance has the id associated correctly for later queries.
    vertex.id = result['id']

    return result['id'], result['existed']


async def get_or_create_edge(g: AsyncGraphTraversalSource, edge: EdgeBase,
                             source_id: int=None, target_id: int=None) -> tuple:
    """Create an edge if not existed before, if the given edge already exists, get its id.

    Optional parameters source_id and target_id are present for optimizations.
    """
    # If source_id/target_id are not provided explicitly and edge.source/edge.target are not set, this will raise
    # an exception. Provide at least one based on your usage.
    source_id = source_id or edge.source.id
    target_id = target_id or edge.target.id

    query = g.V(source_id).outE()
    creation = g.V(source_id).addE(edge.__label__)

    for key, value in edge.to_dict().items():
        if key in ('source', 'target', 'id'):
            continue

        if value is not None:
            query = query.has(key, value)
            creation = creation.property(key, value)
        else:
            query = query.hasNot(key)

    result = await query.as_('e').inV().hasId(target_id).select('e').fold().coalesce(
            unfold().id().as_('id').constant(True).as_('existed').select('id', 'existed'),
            creation.as_('e').to(g.V(target_id)).select('e').id().as_('id')
                .constant(False).as_('existed').select('id', 'existed')
        ).next()

    # Assign to instance so instance has the id associated correctly for later queries.
    edge.id = result['id']

    return result['id'], result['existed']
