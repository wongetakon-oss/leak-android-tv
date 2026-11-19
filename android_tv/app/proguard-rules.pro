# Proguard rules for LK21 Netflix TV
-keepattributes *Annotation*
-keepclassmembers class * {
    @com.google.gson.annotations.SerializedName <fields>;
}
-keep class com.netflix.lk21tv.models.** { *; }
