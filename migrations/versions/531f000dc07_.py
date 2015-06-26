"""visits

Revision ID: 531f000dc07
Revises: 5468bfe37ea
Create Date: 2015-06-26 15:24:34.734124

"""

# revision identifiers, used by Alembic.
revision = '531f000dc07'
down_revision = '5468bfe37ea'

from alembic import op
import sqlalchemy as sa



def upgrade():
	op.add_column('pepe', sa.Column('visits', sa.Integer))

def downgrade():
	op.drop_column('pepe', 'visits')
