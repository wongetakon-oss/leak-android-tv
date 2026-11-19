package com.netflix.lk21tv.ui

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.core.content.ContextCompat
import androidx.leanback.app.BackgroundManager
import androidx.leanback.app.BrowseSupportFragment
import androidx.leanback.widget.*
import androidx.lifecycle.lifecycleScope
import com.bumptech.glide.Glide
import com.netflix.lk21tv.R
import com.netflix.lk21tv.models.CategoryFeed
import com.netflix.lk21tv.models.MovieCard
import com.netflix.lk21tv.network.ApiClient
import kotlinx.coroutines.launch

class MainFragment : BrowseSupportFragment() {

    private lateinit var backgroundManager: BackgroundManager
    private lateinit var rowsAdapter: ArrayObjectAdapter
    private var defaultBackground: Int = R.color.netflix_black

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        setupUI()
        setupBackgroundManager()
        setupEventListeners()
        loadFeeds()
    }

    private fun setupUI() {
        title = getString(R.string.browse_title)
        badgeDrawable = ContextCompat.getDrawable(requireContext(), R.drawable.app_logo)
        
        // Konfigurasi Navigasi Header Ala Netflix
        headersState = HEADERS_ENABLED
        isHeadersTransitionOnBackEnabled = true
        brandColor = ContextCompat.getColor(requireContext(), R.color.netflix_black)
        searchAffordanceColor = ContextCompat.getColor(requireContext(), R.color.netflix_red)

        rowsAdapter = ArrayObjectAdapter(ListRowPresenter())
        adapter = rowsAdapter
    }

    private fun setupBackgroundManager() {
        backgroundManager = BackgroundManager.getInstance(requireActivity()).apply {
            attach(requireActivity().window)
            color = ContextCompat.getColor(requireContext(), defaultBackground)
        }
    }

    private fun setupEventListeners() {
        // Klik pada salah satu poster film (tombol OK pada remote TV)
        onItemViewClickedListener = OnItemViewClickedListener { _, item, _, _ ->
            if (item is MovieCard) {
                val intent = Intent(requireContext(), PlaybackActivity::class.java).apply {
                    putExtra("MOVIE_ID", item.id)
                    putExtra("MOVIE_TITLE", item.title)
                }
                startActivity(intent)
            }
        }

        // Ketika remote menyorot salah satu film (D-Pad navigasi)
        // Ubah latar belakang dinamis seperti Netflix
        setOnItemViewSelectedListener { _, item, _, _ ->
            if (item is MovieCard && item.posterUrl.isNotEmpty()) {
                lifecycleScope.launch {
                    try {
                        Glide.with(requireContext())
                            .asBitmap()
                            .load(item.posterUrl)
                            .into(object : com.bumptech.glide.request.target.CustomTarget<android.graphics.Bitmap>() {
                                override fun onResourceReady(
                                    resource: android.graphics.Bitmap,
                                    transition: com.bumptech.glide.request.transition.Transition<in android.graphics.Bitmap>?
                                ) {
                                    backgroundManager.setBitmap(resource)
                                }
                                override fun onLoadCleared(placeholder: android.graphics.drawable.Drawable?) {}
                            })
                    } catch (e: Exception) {
                        // ignore
                    }
                }
            }
        }
    }

    private fun loadFeeds() {
        lifecycleScope.launch {
            try {
                val feedList = ApiClient.apiService.getHomeFeed()
                populateRows(feedList)
            } catch (e: Exception) {
                e.printStackTrace()
                Toast.makeText(requireContext(), getString(R.string.error_feed), Toast.LENGTH_LONG).show()
                // Jika koneksi gagal, load kategori darurat agar aplikasi tetap berjalan
                loadEmergencyFallback()
            }
        }
    }

    private fun populateRows(feeds: List<CategoryFeed>) {
        rowsAdapter.clear()
        val cardPresenter = CardPresenter()

        for (feed in feeds) {
            val listRowAdapter = ArrayObjectAdapter(cardPresenter)
            for (movie in feed.movies) {
                listRowAdapter.add(movie)
            }
            val header = HeaderItem(feed.id.toLong(), feed.name)
            rowsAdapter.add(ListRow(header, listRowAdapter))
        }
    }

    private fun loadEmergencyFallback() {
        val sampleFeed = listOf(
            CategoryFeed(
                id = 1,
                name = "🔥 Rekomendasi (Mode Offline)",
                movies = listOf(
                    MovieCard("sample-1", "Avatar: The Way of Water", "https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg", "8.2", "4K", ""),
                    MovieCard("sample-2", "Spider-Man: No Way Home", "https://image.tmdb.org/t/p/w500/uJYYizSuA9Y3DCs0qS4qWvlyZz4.jpg", "8.7", "1080p", "")
                )
            )
        )
        populateRows(sampleFeed)
    }
}
