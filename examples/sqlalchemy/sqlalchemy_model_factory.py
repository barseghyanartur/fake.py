from fake import FactoryMethod, ModelFactory, SubFactory
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE_URL = "sqlite:///test_database.db"

ENGINE = create_engine(DATABASE_URL)
SESSION = scoped_session(sessionmaker(bind=ENGINE))

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "SQLAlchemyModelFactory",
    "ENGINE",
    "SESSION",
)


class SQLAlchemyModelFactory(ModelFactory):
    """SQLAlchemy ModelFactory."""

    @classmethod
    def get_session(cls):
        return SESSION()

    @classmethod
    def save(cls, instance):
        session = cls.get_session()
        session.add(instance)
        session.commit()

    @classmethod
    def create(cls, **kwargs):
        session = cls.get_session()

        model = cls.Meta.model
        unique_fields = cls._meta.get("get_or_create", ["id"])

        # Check for existing instance
        if unique_fields:
            query_kwargs = {field: kwargs.get(field) for field in unique_fields}
            instance = session.query(model).filter_by(**query_kwargs).first()
            if instance:
                return instance

        # Construct model_data from class attributes
        model_data = {
            field: (value() if isinstance(value, FactoryMethod) else value)
            for field, value in cls.__dict__.items()
            if (
                not field.startswith("_")
                and not field == "Meta"
                and not getattr(value, "is_trait", False)
                and not getattr(value, "is_pre_save", False)
                and not getattr(value, "is_post_save", False)
            )
        }

        # Separate nested attributes and direct attributes
        nested_attrs = {k: v for k, v in kwargs.items() if "__" in k}
        direct_attrs = {k: v for k, v in kwargs.items() if "__" not in k}

        # Update direct attributes with callable results
        for field, value in model_data.items():
            if isinstance(value, (FactoryMethod, SubFactory)):
                model_data[field] = (
                    value()
                    if field not in direct_attrs
                    else direct_attrs[field]
                )

        # Create a new instance
        instance = model(**model_data)
        cls._apply_traits(instance, **kwargs)

        # Handle nested attributes
        for attr, value in nested_attrs.items():
            field_name, nested_attr = attr.split("__", 1)
            if isinstance(getattr(cls, field_name, None), SubFactory):
                related_instance = getattr(
                    cls, field_name
                ).factory_class.create(**{nested_attr: value})
                setattr(instance, field_name, related_instance)

        # Run pre-save hooks
        pre_save_hooks = [
            method
            for method in dir(cls)
            if getattr(getattr(cls, method), "is_pre_save", False)
        ]
        cls._run_hooks(pre_save_hooks, instance)

        # Save instance
        cls.save(instance)

        # Run post-save hooks
        post_save_hooks = [
            method
            for method in dir(cls)
            if getattr(getattr(cls, method), "is_post_save", False)
        ]
        cls._run_hooks(post_save_hooks, instance)

        return instance
