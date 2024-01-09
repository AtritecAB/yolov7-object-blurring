from libxmp import XMPFiles


def transfer_xmp(source_image_path, target_image_path):
    # Open the source image and get the XMP data
    source_xmpfile = XMPFiles(file_path=source_image_path, open_forupdate=False)
    source_xmp = source_xmpfile.get_xmp()

    # Check if source image has XMP data
    if source_xmp is not None:
        # Open the target image
        target_xmpfile = XMPFiles(file_path=target_image_path, open_forupdate=True)

        # Write the XMP data from the source image to the target image
        target_xmpfile.put_xmp(source_xmp)
        target_xmpfile.close_file()

    # Close the source XMP file
    source_xmpfile.close_file()
