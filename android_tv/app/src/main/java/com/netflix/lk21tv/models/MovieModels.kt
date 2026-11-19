package com.netflix.lk21tv.models

import com.google.gson.annotations.SerializedName
import java.io.Serializable

data class MovieCard(
    @SerializedName("id") val id: String,
    @SerializedName("title") val title: String,
    @SerializedName("poster_url") val posterUrl: String,
    @SerializedName("rating") val rating: String?,
    @SerializedName("quality") val quality: String?,
    @SerializedName("description") val description: String?
) : Serializable

data class CategoryFeed(
    @SerializedName("id") val id: Int,
    @SerializedName("name") val name: String,
    @SerializedName("movies") val movies: List<MovieCard>
) : Serializable

data class MovieDetail(
    @SerializedName("id") val id: String,
    @SerializedName("title") val title: String,
    @SerializedName("overview") val overview: String,
    @SerializedName("rating") val rating: String,
    @SerializedName("year") val year: String,
    @SerializedName("stream_url") val streamUrl: String,
    @SerializedName("poster_url") val posterUrl: String
) : Serializable
