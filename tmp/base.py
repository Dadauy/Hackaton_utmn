#!/usr/bin/env python
import sqlalchemy as sa

engine = sa.create_engine('sqlite://')

meta = sa.MetaData()

users = sa.Table('users', meta,
    sa.Column('id', sa.Integer, 
        primary_key=True, nullable=False, 
        unique=True, index=True),
    sa.Column('full_name', sa.String),
    sa.Column('email', sa.String),
    sa.Column('password', sa.String),
    sa.Column('info', sa.String)
)

projects = sa.Table('projects', meta, 
    sa.Column('id', sa.Integer,
        primary_key=True, nullable=False, 
        unique=True, index=True),
    sa.Column('name', sa.String),
    sa.Column('creator', sa.ForeignKey('users.id')),
    sa.Column('status', sa.String),
    sa.Column('info', sa.String),
    sa.Column('date_planned', sa.DateTime),
    sa.Column('date_actual', sa.DateTime)
)

members = sa.Table('editors', meta,
    sa.Column('type', sa.String),
    sa.Column('proj_id', sa.ForeignKey('projects.id')),
    sa.Column('user_id', sa.ForeignKey('users.id'))
)

nodes = sa.Table('node', meta,
    sa.Column('id', sa.Integer,
        primary_key=True, nullable=False, 
        unique=True, index=True),
    sa.Column('proj_id', sa.ForeignKey('projects.id')),
    sa.Column('type', sa.String),
    sa.Column('status', sa.String),
    sa.Column('info', sa.String),
    sa.Column('date_planned', sa.DateTime),
    sa.Column('date_actual', sa.DateTime)
)

dependencies = sa.Table('dependencies', meta,
    sa.Column('id', sa.Integer,
        primary_key=True, nullable=False, 
        unique=True, index=True),
    sa.Column('proj_id', sa.ForeignKey('projects.id')),
    sa.Column('from', sa.ForeignKey('nodes.id')),
    sa.Column('to', sa.ForeignKey('nodes.id'))
)
