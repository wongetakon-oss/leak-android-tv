package com.netflix.lk21tv.ui

import android.view.ViewGroup
import androidx.core.content.ContextCompat
import androidx.leanback.widget.ImageCardView
import androidx.leanback.widget.Presenter
import com.bumptech.glide.Glide
import com.bumptech.glide.load.resource.drawable.DrawableTransitionOptions
import com.netflix.lk21tv.R
import com.netflix.lk21tv.models.MovieCard

class CardPresenter : Presenter() {

    companion object {
        private const val CARD_WIDTH = 220
        private const val CARD_HEIGHT = 330
    }

    override fun onCreateViewHolder(parent: ViewGroup): ViewHolder {
        val cardView = ImageCardView(parent.context).apply {
            isFocusable = true
            isFocusableInTouchMode = true
            setMainImageDimensions(CARD_WIDTH, CARD_HEIGHT)
            setInfoAreaBackgroundColor(ContextCompat.getColor(context, R.color.netflix_dark_gray))
        }
        return ViewHolder(cardView)
    }

    override fun onBindViewHolder(viewHolder: ViewHolder, item: Any?) {
        val movie = item as? MovieCard ?: return
        val cardView = viewHolder.view as ImageCardView

        cardView.titleText = movie.title
        cardView.contentText = "${movie.rating ?: "7.5"} ★ | ${movie.quality ?: "HD"}"

        Glide.with(viewHolder.view.context)
            .load(movie.posterUrl)
            .centerCrop()
            .transition(DrawableTransitionOptions.withCrossFade())
            .into(cardView.mainImageView)
    }

    override fun onUnbindViewHolder(viewHolder: ViewHolder) {
        val cardView = viewHolder.view as ImageCardView
        cardView.badgeImage = null
        cardView.mainImage = null
    }
}
