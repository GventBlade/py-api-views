from rest_framework import serializers
from cinema.models import Movie, Actor, CinemaHall, Genre


class GenreSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)

    class Meta:
        model = Genre
        fields = (
            "id",
            "name",
        )


class ActorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)

    class Meta:
        model = Actor
        fields = (
            "id",
            "first_name",
            "last_name",
        )


class CinemaHallSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    rows = serializers.IntegerField()
    seats_in_row = serializers.IntegerField()

    class Meta:
        model = CinemaHall
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
        )


class MovieSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    duration = serializers.IntegerField()
    genres = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Genre.objects.all())
    actors = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Actor.objects.all())

    class Meta:
        model = Movie
        fields = (
            "id",
            "title",
            "description",
            "duration",
            "genres",
            "actors",
        )

    def create(self, validated_data):
        genres_data = validated_data.pop("genres", [])
        actors_data = validated_data.pop("actors", [])
        movie = Movie.objects.create(**validated_data)
        movie.genres.set(genres_data)
        movie.actors.set(actors_data)
        return movie

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get(
            "description", instance.description)
        instance.duration = validated_data.get("duration", instance.duration)
        instance.save()
        genres_data = validated_data.get("genres", None)
        actors_data = validated_data.get("actors", None)
        if genres_data is not None:
            instance.genres.set(genres_data)
        if actors_data is not None:
            instance.actors.set(actors_data)

        return instance
