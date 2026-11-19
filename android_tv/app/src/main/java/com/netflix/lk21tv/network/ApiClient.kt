package com.netflix.lk21tv.network

import com.netflix.lk21tv.models.CategoryFeed
import com.netflix.lk21tv.models.MovieCard
import com.netflix.lk21tv.models.MovieDetail
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET
import retrofit2.http.Path
import retrofit2.http.Query
import java.util.concurrent.TimeUnit

interface ApiService {

    @GET("api/feed")
    suspend fun getHomeFeed(): List<CategoryFeed>

    @GET("api/movie/{id}")
    suspend fun getMovieDetail(@Path("id") movieId: String): MovieDetail

    @GET("api/search")
    suspend fun searchMovies(@Query("q") query: String): List<MovieCard>
}

object ApiClient {
    /**
     * CATATAN PENTING ALAMAT IP:
     * - Jika uji coba di Android Emulator: gunakan "http://10.0.2.2:8000/"
     * - Jika diinstal langsung di Android TV fisik: ganti dengan IP lokal laptop/PC Anda,
     *   misalnya "http://192.168.1.15:8000/" (pastikan TV & PC dalam 1 Wi-Fi).
     */
    var BASE_URL = "http://192.168.28.7:8000/"

    private val loggingInterceptor = HttpLoggingInterceptor().apply {
        level = HttpLoggingInterceptor.Level.BODY
    }

    private val okHttpClient = OkHttpClient.Builder()
        .addInterceptor(loggingInterceptor)
        .connectTimeout(15, TimeUnit.SECONDS)
        .readTimeout(15, TimeUnit.SECONDS)
        .build()

    val apiService: ApiService by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ApiService::class.java)
    }
}
