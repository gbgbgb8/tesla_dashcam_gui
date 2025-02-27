# tooltip_data.py

TOOLTIPS = {
    "source_entry": "Folder(s) containing the saved camera files",
    "output_entry": "Path for the new movie file",
    "skip_existing_cb": "Skip creating encoded video file if it already exists (Performance: Faster)",
    "delete_source_cb": "Delete the processed files upon completion (Performance: No impact)",
    "exclude_subdirs_cb": "Do not search sub folders for video files (Performance: Faster)",
    "layout_combo": "Layout of the created video (Performance: No impact)",
    "scale_entry": "Set camera clip scale (Performance: Lower scale is faster)",
    "perspective_cb": "Show side cameras in perspective (Performance: Slightly slower)",
    "background_entry": "Background color for video (Performance: No impact)",
    "show_timestamp_cb": "Show timestamp in video (Performance: Slightly slower)",
    "halign_combo": "Horizontal alignment for timestamp (Performance: No impact)",
    "valign_combo": "Vertical alignment for timestamp (Performance: No impact)",
    "font_entry": "Font file for timestamp (Performance: No impact)",
    "fontsize_entry": "Font size for timestamp (Performance: No impact)",
    "fontcolor_entry": "Font color for timestamp (Performance: No impact)",
    "quality_combo": "Define the quality setting for the video (Performance: Lower is faster)",
    "compression_combo": "Speed to optimize video (Performance: Faster is quicker, but larger file size)",
    "fps_entry": "Frames per second for resulting video (Performance: Lower is faster)",
    "encoding_combo": "Encoding to use for video creation (Performance: x264 is faster, x265 is slower but smaller file size)",
    "gpu_cb": "Use GPU acceleration (Performance: Faster, but may have issues on Apple Silicon)",
    "motion_only_cb": "Fast-forward through video when there is no motion (Performance: Faster)",
    "merge_cb": "Merge the video files from different folders into 1 big video file (Performance: Slower, but convenient)",
    "merge_template_entry": "Template string to group events in different video files",
    "merge_timestamp_format_entry": "Format for timestamps in merge_template",
    "keep_intermediate_cb": "Do not remove the clip video files that are created (Performance: No impact, but uses more disk space)",
    "keep_events_cb": "Do not remove the event video files when merging events (Performance: No impact, but uses more disk space)",
    "moviefile_timestamp_combo": "Match modification timestamp of resulting video files to event timestamp (Performance: No impact)",
    "slowdown_entry": "Slow down video output (e.g., 2 means half speed) (Performance: Slower)",
    "speedup_entry": "Speed up the video (e.g., 2 means twice the speed) (Performance: Faster)",
    "chapter_offset_entry": "Offset in seconds for chapters in merged video (Performance: No impact)",
}