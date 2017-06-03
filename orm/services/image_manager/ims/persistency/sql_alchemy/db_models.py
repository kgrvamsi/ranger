###
# This file was generated by ProCG version 2.0
#
# File name:   ims\persitency\sql_alchemy\db_models.py
# Language:    Python 2.7
# Database:    My Sql
#
# Copyright (c) 2002-2016 iGenXSoft.
# For more information visit http://www.igenxsoft.com
###

from sqlalchemy import (Column, Integer, SmallInteger, String,
                        ForeignKeyConstraint)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from oslo_db.sqlalchemy import models

from ims.logger import get_logger
from orm_common.utils.cross_api_utils import get_regions_of_group, set_utils_conf
from pecan import conf
from ims.logic.error_base import NotFoundError
from ims.logic.error_base import ErrorStatus
Base = declarative_base()

LOG = get_logger(__name__)


class IMSBaseModel(models.ModelBase):

    """Base class from IMS Models."""

    __table_args__ = {'mysql_engine': 'InnoDB'}


class Image(Base, IMSBaseModel):
    ###
    # Image is a DataObject and contains all the fields defined in Image table
    # record. Defined as SqlAlchemy model map to a table
    ###
    __tablename__ = "image"

    def __init__(self,
                 id=None,
                 name=None,
                 enabled=None,
                 url=None,
                 protected=None,
                 visibility=None,
                 disk_format=None,
                 container_format=None,
                 min_disk=None,
                 min_ram=None,
                 owner=None,
                 schema=None,
                 created_at=None,
                 updated_at=None):

        self.id = id
        self.name = name
        self.enabled = enabled
        self.url = url
        self.protected = protected
        self.visibility = visibility
        self.disk_format = disk_format
        self.container_format = container_format
        self.min_disk = min_disk
        self.min_ram = min_ram
        self.owner = owner
        self.schema = schema
        self.created_at = created_at
        self.updated_at = updated_at

    id = Column(String, primary_key=True)
    name = Column(String)
    enabled = Column(SmallInteger)
    url = Column(String)
    protected = Column(SmallInteger)
    visibility = Column(String)
    disk_format = Column(String)
    container_format = Column(String)
    min_disk = Column(Integer)
    min_ram = Column(Integer)
    owner = Column(String)
    schema = Column(String)
    created_at = Column(Integer)
    updated_at = Column(Integer)
    properties = relationship("ImageProperty", uselist=True,
                              cascade="all, delete, delete-orphan",
                              primaryjoin="and_(Image.id==ImageProperty.image_id)")
    regions = relationship("ImageRegion", uselist=True,
                           cascade="all, delete, delete-orphan",
                           primaryjoin="and_(Image.id==ImageRegion.image_id)")
    tags = relationship("ImageTag", uselist=True,
                        cascade="all, delete, delete-orphan",
                        primaryjoin="and_(Image.id==ImageTag.image_id)")
    customers = relationship("ImageCustomer",
                             uselist=True,
                             cascade="all, delete, delete-orphan",
                             primaryjoin="and_(Image.id==ImageCustomer.image_id)")

    def __json__(self):
        properties = {}
        # don't send tags to rds server
        # tags = {}

        for prop in self.properties:
            properties[prop.key_name] = prop.key_value

        return dict(
            id=self.id,
            name=self.name,
            enabled=self.enabled * 1,
            url=self.url,
            protected=self.protected * 1,
            visibility=self.visibility,
            disk_format=self.disk_format,
            container_format=self.container_format,
            min_disk=self.min_disk,
            min_ram=self.min_ram,
            owner=self.owner,
            schema=self.schema,
            created_at=self.created_at,
            updated_at=self.updated_at,
            properties=properties,
            regions=self.get_regions_json(),
            customers=[customer.__json__() for customer in self.customers]
        )

    def get_proxy_dict(self):
        proxy_dict = self.__json__()

        return proxy_dict

    def get_regions_json(self):
        regions_json = []
        for region in self.regions:
            region_json = region.__json__()
            regions_json.append(region_json)
        return regions_json

    def get_existing_region_names(self):
        existing_region_names = []
        for region in self.get_proxy_dict()['regions']:
            existing_region_names.append(region['name'])
        return existing_region_names

    def add_region(self, image_region):
        assert isinstance(image_region, ImageRegion)
        try:
            LOG.debug("add region {0} to image {1}".format(str(image_region),
                                                           str(self)))
            region_list = filter(lambda region: region.region_name == image_region.region_name, self.regions)
            if len(region_list) > 0:
                raise ErrorStatus(409, "Region {} already exist in Image {}".format(image_region.region_name, self.name))
            self.regions.append(image_region)

        except Exception as exception:
            LOG.log_exception("Failed to add region {0} to image {1}".format(
                str(image_region), str(self)), exception)
            raise

    def remove_region(self, region_name):
        assert isinstance(region_name, basestring)
        try:
            LOG.debug("remove regions {0} from image {1}".format(region_name,
                                                                 str(self)))
            region_found = False
            for region in reversed(self.regions):
                if region.region_name == region_name:
                    self.regions.remove(region)
                    region_found = True

            if not region_found:
                raise NotFoundError("Region {} not found in Image {} (name - {}) ".format(region_name, self.id, self.name))

        except Exception as exception:
            LOG.log_exception(
                "Failed to remove region {0} from image {1}".format(
                    region_name, str(self)), exception)
            raise

    def remove_all_regions(self):
        try:
            LOG.debug("remove regions from image {0}".format(str(self)))
            for region in reversed(self.regions):
                    self.regions.remove(region)

        except Exception as exception:
            LOG.log_exception("Failed to remove regions from image {0}".format(str(self)), exception)
            raise

    def add_customer(self, image_customer):
        assert isinstance(image_customer, ImageCustomer)
        try:
            LOG.debug("add customer {0} to image {1}".format(str(image_customer), str(self)))
            self.customers.append(image_customer)

        except Exception as exception:
            LOG.log_exception("Failed to add customer {0} from image {1}".format(str(image_customer), str(self)), exception)

    def remove_customer(self, customer_id):
        assert isinstance(customer_id, basestring)
        try:
            LOG.debug("remove customers {0} from image {1}".format(customer_id,
                                                                   str(self)))

            for customer in reversed(self.customers):
                if customer.customer_id == customer_id:
                    self.customers.remove(customer)

        except Exception as exception:
            LOG.log_exception(
                "Failed to remove customer {0} from image {1}".format(
                    customer_id, str(self)), exception)

    def remove_all_customers(self):
        try:
            LOG.debug("remove customers from image {0}".format(str(self)))

            for customer in reversed(self.customers):
                    self.customers.remove(customer)

        except Exception as exception:
            LOG.log_exception("Failed to remove customers from image"
                              " {0}".format(str(self)), exception)

    def __repr__(self):
        text = "Image(id='{}', name='{}', enabled={}, url='{}', " \
               "protected='{}', visibility='{}', disk_format='{}', " \
               "container_format='{}', min_disk={}, min_ram={}, owner='{}', " \
               "schema='{}', created_at='{}', updated_at='{}')"\
            .format(self.id, self.name, self.enabled, self.url, self.protected,
                    self.visibility, self.disk_format, self.container_format,
                    self.min_disk, self.min_ram, self.owner, self.schema,
                    self.created_at, self.updated_at)
        return text


class ImageProperty(Base, IMSBaseModel):
    ###
    # ImageProperty is a DataObject and contains all the fields defined in
    # ImageProperty table record. Defined as SqlAlchemy model map to a table
    ###
    __tablename__ = "image_property"

    def __init__(self,
                 image_id=None,
                 key_name=None,
                 key_value=None):

        self.image_id = image_id
        self.key_name = key_name
        self.key_value = key_value

    image_id = Column(String, primary_key=True)
    key_name = Column(String, primary_key=True)
    key_value = Column(String)
    image = relationship("Image", uselist=False,
                         primaryjoin="and_(ImageProperty.image_id==Image.id)")
    __table_args__ = (
        ForeignKeyConstraint(
            ["image_id"],
            ["image.id"],
            name="image_properties_ibfk_1"
        ),
    )

    def __json__(self):
        return dict(
            image_id=self.image_id,
            key_name=self.key_name,
            key_value=self.key_value
        )

    def __repr__(self):
        text = "ImageProperty(image_id='{}', key_name='{}'," \
               " key_value='{}')".format(self.image_id, self.key_name,
                                         self.key_value)
        return text


class ImageRegion(Base, IMSBaseModel):
    ###
    # ImageRegion is a DataObject and contains all the fields defined in
    # ImageRegion table record. Defined as SqlAlchemy model map to a table
    ###
    def __init__(self, region_name=None, region_type=None,
                 checksum="", size="", virtual_size=""):
        Base.__init__(self)
        self.region_name = region_name
        self.region_type = region_type
        self.checksum = checksum
        self.size = size
        self.virtual_size = virtual_size

    __tablename__ = "image_region"

    image_id = Column(String, primary_key=True)
    region_name = Column(String, primary_key=True)
    region_type = Column(String)
    checksum = Column(String)
    size = Column(String)
    virtual_size = Column(String)
    image = relationship("Image", uselist=False,
                         primaryjoin="and_(ImageRegion.image_id==Image.id)")
    __table_args__ = (
        ForeignKeyConstraint(
            ["image_id"],
            ["image.id"],
            name="image_region_ibfk_1"
        ),
    )

    def __json__(self):
        return dict(
            image_id=self.image_id,
            name=self.region_name,
            type=self.region_type,
            checksum=self.checksum,
            size=self.size,
            virtual_size=self.virtual_size
        )

    @staticmethod
    def get_group_regions(group_name):
        set_utils_conf(conf)
        regions = get_regions_of_group(group_name)
        return regions

    def __repr__(self):
        text = "ImageRegion(image_id='{}', region_name='{}'," \
               "region_type='{}', checksum='{}', size='{}'," \
               "virtual_size='{}')".format(self.image_id, self.region_name,
                                           self.region_type, self.checksum,
                                           self.size, self.virtual_size)
        return text


class ImageTag(Base, IMSBaseModel):
    ###
    # ImageTag is a DataObject and contains all the fields defined in ImageTag
    # table record. Defined as SqlAlchemy model map to a table
    ###
    __tablename__ = "image_tag"

    def __init__(self,
                 image_id=None,
                 tag=None):

        self.image_id = image_id
        self.tag = tag

    image_id = Column(String, primary_key=True)
    tag = Column(String, primary_key=True)
    __table_args__ = (
        ForeignKeyConstraint(
            ["image_id"],
            ["image.id"],
            name="image_tags_ibfk_1"
        ),
    )

    def __json__(self):
        return dict(
            image_id=self.image_id,
            tag=self.tag
        )

    def __repr__(self):
        text = "ImageTag(image_id='{}', tag='{}')".format(
            self.image_id, self.tag)
        return text


class ImageCustomer(Base, IMSBaseModel):
    ###
    # ImageCustomer is a DataObject and contains all the fields defined in
    # ImageCustomer table record. Defined as SqlAlchemy model map to a table
    ###
    __tablename__ = "image_customer"

    def __init__(self,
                 image_id=None,
                 customer_id=None):

        self.image_id = image_id
        self.customer_id = customer_id

    image_id = Column(String, primary_key=True)
    customer_id = Column(String, primary_key=True)
    __table_args__ = (
        ForeignKeyConstraint(
            ["image_id"],
            ["image.id"],
            name="image_customer_ibfk_1"
        ),
    )

    def __json__(self):
        return dict(
            image_id=self.image_id,
            customer_id=self.customer_id
        )

    def __repr__(self):
        text = "ImageCustomer(image_id='{}', customer_id='{}')".format(
            self.image_id, self.customer_id)
        return text