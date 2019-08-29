import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from application.views.authentication import get_token_from_header, get_user_id_from_token
from flask import abort, current_app
from application.models import FoodTruck, User, db
from sqlalchemy.exc import SQLAlchemyError


class FoodTruckObject(SQLAlchemyObjectType):
    """
    A class used to encapsulate the GraphQL endpoint
    """
    class Meta:
        model = FoodTruck
        interfaces = (graphene.relay.Node, )


class CreateFoodTruck(graphene.Mutation):
    """
    A class used to encapsulate the GraphQL mutation for creating food trucks
    """
    class Arguments:
        name = graphene.String(required=True)
        longitude = graphene.Float(required=True)
        latitude = graphene.Float(required=True)
        days_hours = graphene.String(required=True)
        food_items = graphene.String(required=True)


    food_truck = graphene.Field(lambda: FoodTruckObject)


    def mutate(self, info, name, longitude, latitude, days_hours, food_items):
        # get authentication token from request header
        auth_token = get_token_from_header()

        # return unauthorized if token is not present
        if not auth_token:
            abort(401, 'A valid token must be included')

        # get the user_id from the token
        user_id = get_user_id_from_token(auth_token)

        # create and insert entry in database
        try:
            truck=FoodTruck(
                name = name,
                longitude = longitude,
                latitude = latitude,
                days_hours = days_hours,
                food_items = food_items,
                user_id = user_id
            )
            db.session.add(truck)
            db.session.commit()
            current_app.logger.info('successfully inserted food truck entry with id %d', truck.uuid)
            return CreateFoodTruck(food_truck=truck)
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error('error inserting food truck entry (%s, %d, %d, %s, %s): %s', 
                            name, latitude, longitude, days_hours, food_items, e)
            abort(500, 'Error creating resource')


class UpdateFoodTruck(graphene.Mutation):
    """
    A class used to encapsulate the GraphQL mutation for updating food trucks
    """
    class Arguments:
        truck_id = graphene.Int(required=True)
        name = graphene.String(required=True)
        longitude = graphene.Float(required=True)
        latitude = graphene.Float(required=True)
        days_hours = graphene.String(required=True)
        food_items = graphene.String(required=True)


    food_truck = graphene.Field(lambda: FoodTruckObject)


    def mutate(self, info, truck_id, name, longitude, latitude, days_hours, food_items):
        # get authentication token from request header
        auth_token = get_token_from_header()

        # return unauthorized if token is not present
        if not auth_token:
            abort(401, 'A valid token must be included')

        # get the user_id from the token
        user_id = get_user_id_from_token(auth_token)

        # fetch truck by id and update or create if it does not exist
        try:
            truck = FoodTruck.query.filter_by(uuid=truck_id).first()

            # truck does not exist, so it is created
            if truck is None:
                truck = FoodTruck(
                    name = name,
                    longitude = longitude,
                    latitude = latitude,
                    days_hours = days_hours,
                    food_items = food_items,
                    user_id = user_id
                )
                truck.uuid = truck_id
                db.session.add(truck)
            # truck exists, so it is updated
            else:
                if truck.user_id == user_id or User.is_admin(user_id):
                    truck.name = name
                    truck.longitude = longitude
                    truck.latitude = latitude
                    truck.days_hours = days_hours
                    truck.food_items = food_items
                else:
                    abort(401, 'Not authorized to modify this resource')
            # commit changes to database
            db.session.commit()
            current_app.logger.info('successfully updated food truck entry id %d', truck_id)
            return UpdateFoodTruck(food_truck=truck)
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error('error updating food truck entry id %d: %s', truck_id, e)
            abort(500, 'Error updating resource with id {}'.format(truck_id))


class DeleteFoodTruck(graphene.Mutation):
    """
    A class used to encapsulate the GraphQL mutation for deleting food trucks
    """
    class Arguments:
        truck_id = graphene.Int(required=True)


    food_truck = graphene.Field(lambda: FoodTruckObject)


    def mutate(self, info, truck_id):
        # get authentication token from request header
        auth_token = get_token_from_header()

        # return unauthorized if token is not present
        if not auth_token:
            abort(401, 'A valid token must be included')

        # get the user_id from the token
        user_id = get_user_id_from_token(auth_token)

        # delete truck with id if it exists
        try:
            truck = FoodTruck.query.filter_by(uuid=truck_id).first()
            if truck:
                if truck.user_id == user_id or User.is_admin(user_id):
                    FoodTruck.query.filter_by(uuid=truck_id).delete()
                    db.session.commit()
                    current_app.logger.info('successfully deleted food truck entry id %d', truck_id)
                    return DeleteFoodTruck(food_truck=truck)
                else:
                    abort(401, 'Not authorized to modify this resource')
            else:
                return DeleteFoodTruck(food_truck=truck)
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error('error deleting food truck entry id %d: %s', truck_id, e)
            abort(500, 'Error deleting resource with id {}'.format(truck_id))  


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_food_trucks = SQLAlchemyConnectionField(FoodTruckObject)


class Mutation(graphene.ObjectType):
    create_food_truck = CreateFoodTruck.Field()
    update_food_truck = UpdateFoodTruck.Field()
    delete_food_truck = DeleteFoodTruck.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)