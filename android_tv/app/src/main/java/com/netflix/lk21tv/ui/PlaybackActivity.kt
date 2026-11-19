package com.netflix.lk21tv.ui

import android.net.Uri
import android.os.Bundle
import android.view.KeyEvent
import android.widget.TextView
import android.widget.Toast
import androidx.fragment.app.FragmentActivity
import androidx.lifecycle.lifecycleScope
import androidx.media3.common.MediaItem
import androidx.media3.common.util.UnstableApi
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.ui.PlayerView
import com.netflix.lk21tv.R
import com.netflix.lk21tv.network.ApiClient
import kotlinx.coroutines.launch

@UnstableApi
class PlaybackActivity : FragmentActivity() {

    private var player: ExoPlayer? = null
    private lateinit var playerView: PlayerView
    private var movieTitle: String? = null
    private var movieId: String? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_playback)

        playerView = findViewById(R.id.player_view)
        movieId = intent.getStringExtra("MOVIE_ID")
        movieTitle = intent.getStringExtra("MOVIE_TITLE") ?: "Sedang Memutar"

        val titleView = findViewById<TextView>(R.id.player_movie_title)
        titleView?.text = movieTitle

        initializePlayer()
        fetchStreamAndPlay()
    }

    private fun initializePlayer() {
        player = ExoPlayer.Builder(this).build().also { exoPlayer ->
            playerView.player = exoPlayer
            exoPlayer.playWhenReady = true
        }
    }

    private fun fetchStreamAndPlay() {
        val id = movieId ?: return
        lifecycleScope.launch {
            try {
                val detail = ApiClient.apiService.getMovieDetail(id)
                playMedia(detail.streamUrl)
            } catch (e: Exception) {
                e.printStackTrace()
                Toast.makeText(this@PlaybackActivity, "Gagal memuat stream. Memutar video demo...", Toast.LENGTH_SHORT).show()
                playMedia("https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4")
            }
        }
    }

    private fun playMedia(url: String) {
        val mediaItem = MediaItem.fromUri(Uri.parse(url))
        player?.setMediaItem(mediaItem)
        player?.prepare()
        player?.play()
    }

    override fun dispatchKeyEvent(event: KeyEvent): Boolean {
        if (event.action == KeyEvent.ACTION_DOWN) {
            when (event.keyCode) {
                KeyEvent.KEYCODE_DPAD_LEFT -> {
                    player?.let {
                        val current = it.currentPosition
                        it.seekTo((current - 10000).coerceAtLeast(0))
                    }
                    playerView.controllerShowTimeoutMs = 3000
                    playerView.showController()
                    return true
                }
                KeyEvent.KEYCODE_DPAD_RIGHT -> {
                    player?.let {
                        val current = it.currentPosition
                        val duration = it.duration
                        it.seekTo((current + 10000).coerceAtMost(duration))
                    }
                    playerView.controllerShowTimeoutMs = 3000
                    playerView.showController()
                    return true
                }
                KeyEvent.KEYCODE_DPAD_CENTER, KeyEvent.KEYCODE_ENTER -> {
                    if (player?.isPlaying == true) {
                        player?.pause()
                    } else {
                        player?.play()
                    }
                    playerView.controllerShowTimeoutMs = 3000
                    playerView.showController()
                    return true
                }
                KeyEvent.KEYCODE_BACK -> {
                    finish()
                    return true
                }
            }
        }
        return super.dispatchKeyEvent(event)
    }

    override fun onPause() {
        super.onPause()
        player?.pause()
    }

    override fun onDestroy() {
        super.onDestroy()
        player?.release()
        player = null
    }
}
