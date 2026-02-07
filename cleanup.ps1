# Files to delete - test, debug, backup, and temporary files

# Backup files
Remove-Item "app.py.backup" -ErrorAction SilentlyContinue
Remove-Item "app_original_backup.py" -ErrorAction SilentlyContinue
Remove-Item "replicate_helper_instantid_backup.py" -ErrorAction SilentlyContinue

# Test files
Remove-Item "test_*.py" -ErrorAction SilentlyContinue
Remove-Item "test_*.txt" -ErrorAction SilentlyContinue
Remove-Item "test_*.log" -ErrorAction SilentlyContinue
Remove-Item "test_face_image.png" -ErrorAction SilentlyContinue

# Debug and diagnostic files
Remove-Item "debug_issue.py" -ErrorAction SilentlyContinue
Remove-Item "diag_replicate.py" -ErrorAction SilentlyContinue
Remove-Item "direct_test.py" -ErrorAction SilentlyContinue
Remove-Item "check_model_inputs.py" -ErrorAction SilentlyContinue
Remove-Item "verify_replicate_token.py" -ErrorAction SilentlyContinue
Remove-Item "verify_setup.py" -ErrorAction SilentlyContinue

# Search and find scripts (development only)
Remove-Item "find_models.py" -ErrorAction SilentlyContinue
Remove-Item "find_working_model.py" -ErrorAction SilentlyContinue
Remove-Item "list_image_models.py" -ErrorAction SilentlyContinue
Remove-Item "search_*.py" -ErrorAction SilentlyContinue

# Temporary output files
Remove-Item "detailed.txt" -ErrorAction SilentlyContinue
Remove-Item "error_log.txt" -ErrorAction SilentlyContinue
Remove-Item "upload_output.txt" -ErrorAction SilentlyContinue

# Unused helper files
Remove-Item "replicate_instruct_pix2pix.py" -ErrorAction SilentlyContinue
Remove-Item "openai_helper.py" -ErrorAction SilentlyContinue

# Upload scripts (no longer needed after upload)
Remove-Item "upload_template.py" -ErrorAction SilentlyContinue
Remove-Item "upload_all_templates.py" -ErrorAction SilentlyContinue
Remove-Item "upload_backend_templates.py" -ErrorAction SilentlyContinue

# Downloaded template (already on Cloudinary)
Remove-Item "superman_backend_template.png" -ErrorAction SilentlyContinue

Write-Host "Cleanup complete!"
