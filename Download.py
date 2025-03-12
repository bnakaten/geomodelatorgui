import streamlit as st
import zipfile

class Download:
    gbs = {}

    def __init__(self, tabMenu):
        self.gb = st.session_state.GLOBALS

        input_path = st.session_state.configuration['config']['base'] + \
            st.session_state.configuration['config']['inputPath']
        output_path = st.session_state.configuration['config']['base'] + \
            st.session_state.configuration['config']['outputPath']

        with open(input_path + self.gb.file['download']['inputFilename'], 'rb') as file:
            zip = zipfile.ZipFile(input_path + self.gb.file['download']['inputFilename'])
            tabMenu.download_button(
                self.gb.button['download']['inputFilenameLable'],
                file,
                file_name = self.gb.file['download']['inputFilename'],
                help="Zip archive contains the following files:\n- " + '\n- '.join(zip.namelist())
            )
            file.close()

        with open(output_path + self.gb.file['download']['outputFilename'], 'rb') as file:
            zip = zipfile.ZipFile(input_path + self.gb.file['download']['outputFilename'])
            tabMenu.download_button(
                self.gb.button['download']['outputFilenameLable'],
                file,
                file_name = self.gb.file['download']['outputFilename'],
                help="Zip archive contains the following files:\n- " + '\n- '.join(zip.namelist())
            )
            file.close()

    @staticmethod
    def download_button(path, filename, mime):
        buffer = Download.file_to_download(path + filename)
        st.download_button(
            filename,
            data = buffer,
            file_name = filename,
            mime = mime
        )

    @staticmethod
    def file_to_download(filename):
        return open(filename, 'rb').read()