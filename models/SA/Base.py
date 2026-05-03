#                      字段    整数      字符串  布尔值    时间      json 
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from sqlalchemy import Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Timestamp_Mixin:
    create_time = Column(DateTime, default=datetime.now, comment='创建时间')
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')


role_user = Table(
    "role_user",
    Base.metadata,
    Column("role_id",ForeignKey("role.id"),primary_key=True),
    Column("user_id",ForeignKey("user.id"),primary_key=True),
)

role_access = Table(
    "role_access",
    Base.metadata,
    Column("role_id",ForeignKey("role.id"),primary_key=True),
    Column("access_id",ForeignKey("access.id"),primary_key=True),
)


class Role(Timestamp_Mixin, Base):
    __tablename__ = "role"
    __table_args__ = {'comment': "角色表"}
    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(15), nullable=False, comment="角色名称")
    role_status = Column(Boolean, default=False, comment="True:启用 False:禁用")
    role_desc = Column(String(255), nullable=True, comment='角色描述')
    users = relationship("User", secondary="role_user", back_populates="roles")
    accesses = relationship("Access", secondary="role_access", back_populates="roles")
                            #back_populates="roles"是其他关联的表中Role表的名字


class User(Timestamp_Mixin, Base):
    __tablename__ = "user"
    __table_args__ = {'comment': "用户表"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), nullable=True, comment="用户名")
    user_type = Column(Boolean, default=False, comment="用户类型 True:超级管理员 False:普通管理员")
    password = Column(String(255), nullable=True)
    nickname = Column(String(255), default='binkuolo', comment='昵称')
    user_phone = Column(String(11), nullable=True, comment='手机号')
    user_email = Column(String(255), nullable=True, comment='邮箱')
    full_name = Column(String(255), nullable=True, comment='姓名')
    user_status = Column(Integer, default=0, comment='0未激活 1正常 2禁用')
    header_img = Column(String(255), nullable=True, comment='头像')
    sex = Column(Integer, default=0, nullable=True, comment='0未知 1男 2女')
    remarks = Column(String(30), nullable=True, comment="备注")
    client_host = Column(String(19), nullable=True, comment="访问IP")
    roles = relationship("Role", secondary="role_user", back_populates="users")


class Access(Timestamp_Mixin, Base):
    __tablename__ = "access"
    __table_args__ = {'comment': "权限表"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    access_name = Column(String(15), nullable=False, comment="权限名称")
    parent_id = Column(Integer, default=0, comment='父id')
    scopes = Column(String(255), unique=True, nullable=False, comment='权限范围标识')
    access_desc = Column(String(255), nullable=True, comment='权限描述')
    menu_icon = Column(String(255), nullable=True, comment='菜单图标')
    is_check = Column(Boolean, default=False, comment='是否验证权限 True为验证 False不验证')
    is_menu = Column(Boolean, default=False, comment='是否为菜单 True菜单 False不是菜单')
    roles = relationship("Role", secondary="role_access", back_populates="accesses")


class AccessLog(Timestamp_Mixin, Base):
    __tablename__ = "access_log"
    __table_args__ = {'comment': "用户操作记录表"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, comment="用户ID")
    target_url = Column(String(255), nullable=True, comment="访问的url")
    user_agent = Column(String(255), nullable=True, comment="访问UA")
    request_params = Column(JSON, nullable=True, comment="请求参数get|post")
    ip = Column(String(32), nullable=True, comment="访问IP")
    note = Column(String(255), nullable=True, comment="备注")

