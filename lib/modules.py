import lib.const as const
from lib.launcher import launch_chrome, long_wait, wait_for_download_path
import json
import numpy as np
import requests
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import os
from random import randint
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import logging

# Logs
l_NEW_SEARCH = '** new search **'
l_results_data_served = '** data_served **'
l_TRANCE_ID_TO_GENE_NAME = 'trance_id to gene name fetched'
l_ENSAMBL_DOWNLOAD = 'downloading ensamle'
l_mir_seq_to_name_success = 'mir_seq_to_name success'
l_mir_seq_to_name_fail = 'mir_seq_to_name fail'
l_MIR_NAME_TO_SEQ = 'mir_name_to_seq'
l_MIRDB = 'get_mir_raw_data'
l_DIANA = 'get_diana_data'
# URL's
u_ENSAMBL = 'http://www.ensembl.org/biomart/martview' \
            '/5706fb700a88a051af6e83eeb866cf0d?VIRTUALSCHEMANAME=default' \
            '&ATTRIBUTES=hsapiens_gene_ensembl.default.feature_page' \
            '.ensembl_transcript_id|hsapiens_gene_ensembl.default' \
            '.feature_page.external_gene_name|hsapiens_gene_ensembl.default' \
            '.feature_page.description|hsapiens_gene_ensembl.default' \
            '.feature_page.phenotype_description|hsapiens_gene_ensembl' \
            '.default.feature_page.ensembl_gene_id&FILTERS=&VISIBLEPANEL' \
            '=resultspanel '
u_MIRDB = 'http://mirdb.org/custom.html'
u_DIANA = 'http://diana.imis.athena-innovation.gr/DianaTools/index.php?r' \
          '=mrmicrot/index'
u_MIRBASE = 'https://www.mirbase.org/search.shtml'
u_MIRBASE_SEQ_QUERY = 'https://www.mirbase.org/cgi-bin/get_seq.pl?acc='
# General
NOT_FOUND_CHAR = -1
NEW_ROW = "\n"
HUMAN_MIR_PRE = 'hsa'
MIR_NAME_KEY = 'mir_name_key'
SEARCH_ID_KEY = 'search_id'
MIR_SEQ_KEY = 'mir_key'
# file names
f_DIANA_RAW_FOLDER = "dianaDB_raw"
f_history_folder = 'search_history'
f_data_tables_folder = 'lib\data tables'
f_MIRDB_CSV = 'mirdb.csv'
f_DIANA_CSV = 'diana.csv'
p_META = 'meta'
p_GENE_EXPRESSION = 'normal_tissue.tsv'
# Ensembl
p_ENSEMBL = 'ensembl'
p_MART_EXPORT_CSV = 'mart_export.csv'
c_TRANS_ID = 'Transcript stable ID'
c_GENE_ID = 'Gene stable ID'
START_COMMENT = '['
c_GENE_DESCRIPTION = 'Gene description'
c_PHENO_DESCRIPTION = 'Phenotype description'
# miRDB Constants
TABLE_ROW_TAG = 'tr'
GENE_TR_LINES_NUMBER = 3
# Diana Constants
DATA_ROW_PREFIX = '>'
GRADE_ROUND_DIG = 0
DATA_ROW_SEP = '|'
# Df columns
c_GRADE = 'grade'
c_INFO = 'info'
c_GENE = 'gene'
c_REL_GRADE = 'Rel grade'
c_REL_GRADE_M = 'Mir rel. grade'
c_REL_GRADE_D = 'Diana rel. Grade'
c_GRADE_M = 'MirDB grade'
c_GRADE_D = 'Diana grade'
c_REL_GRADE_AVG = 'Avg rel. Grade'
c_GRADE_AVG = 'Avg grade'
c_EXP_LEVEL = 'Level'
c_EXP_CELL_TYPE = 'Cell type'
c_exp_tissue = 'Tissue'
# XPATH's
#   Diana
x_d_accept_cookies = '/html/body/div[1]/div[6]/div[2]'
x_d_insert_box = '/html/body/div[1]/div[4]/div/div[2]/div/form/div[3]/textarea'
x_d_submit = '/html/body/div[1]/div[4]/div/div[2]/div/form/input'
x_d_download_results = '/html/body/div[1]/div[4]/div/div[3]/div/div/div/div[' \
                       '1]/div[4]/a'
#   MirDB
x_m_insert_box = '/html/body/table[2]/tbody/tr/td[3]/form/table/tbody/tr[4]/td/textarea'
x_m_submit = '/html/body/table[2]/tbody/tr/td[3]/form/table/tbody/tr[5]/td/input[1]'
x_m_warning = '/html/body/table[2]/tbody/tr/td[3]/h2/font'
x_m_get_results = '/html/body/form/input[2]'
#   Eensembl
x_e_download = '/html/body/div[1]/div/div[3]/div[1]/div/form/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/div/table/tbody/tr/td/div[5]/table/tbody/tr[1]/td/div/table/tbody/tr[1]/td[2]/input[2]'
x_e_get_results = '/html/body/div[1]/div/div[3]/div[1]/div/form/table/tbody/tr[1]/td/div/table/tbody/tr/td[1]/a[3]'
#   MirBase
x_MIR_NAME_ENTRY = '/html/body/div[2]/div[1]/form/input[1]'
x_MIR_FILTER = '/html/body/div[2]/div[2]/div[2]/div/div[2]/label/input'
x_RESULTS_DIV_ID = 'resultTable'
x_MIR_SEQ_ENTRY = '/html/body/div[2]/div[4]/form/table/tbody/tr[' \
                  '3]/td[1]/textarea'
x_SEQ_ENTRY_SUBMIT = '/html/body/div[2]/div[4]/form/table/tbody/tr[' \
                     '3]/td[1]/p[3]/input[1]'
x_SEQ_HSA_FILTER = '/html/body/div[2]/div[4]/form/table/tbody/tr[3]/td[2]/table/tbody/tr[6]/td[2]/input[1]'
x_seq_results = '/html/body/div[2]/div[1]/table'


def validate_search_key_type(key) -> str:
    if len(key) == 13 and key[6] == '_':
        return SEARCH_ID_KEY
    elif 'mir' in key.lower():
        return MIR_NAME_KEY
    return MIR_SEQ_KEY


def get_higher_levels(level) -> list:
    LEVELS = ['Not detected', 'Low', 'Medium', 'High']
    if not level: return LEVELS
    ind = LEVELS.index(level)
    return LEVELS[ind:]


def get_diana_data(mir, temp_foler_name) -> pd.DataFrame:
    def download_diana_raw(mir, download_path):
        '''
        for some reason the download doesnt work on not headless driver
        so there is no DEBUG mode for that function
        :param mir:
        :param download_path:
        :return:
        '''
        url = u_DIANA
        driver, wait = launch_chrome(url, True,
                                     download_folder=download_path)
        accept_cookies = wait.until(EC.element_to_be_clickable(
            (By.XPATH, x_d_accept_cookies))).click()
        insert_box = driver.find_element_by_xpath(x_d_insert_box).send_keys(
            mir)
        submit = driver.find_element_by_xpath(x_d_submit).click()
        download_results = long_wait(wait, x_d_download_results).click()
        driver.switch_to.alert.accept()
        return wait_for_download_path(download_path)

    def parse_row(row):
        row_dict = {}
        if row[0] == DATA_ROW_PREFIX:
            row = row[1:].split(DATA_ROW_SEP)
            if GRADE_ROUND_DIG != 0:
                row_dict[c_GRADE] = round(float(row[2]) * 100, GRADE_ROUND_DIG)
            else:
                row_dict[c_GRADE] = round(float(row[2]) * 100)
            row_dict[c_GENE] = row[1]
        return row_dict

    download_path = os.getcwd() + '\\' + temp_foler_name + '\\' + f_DIANA_RAW_FOLDER
    os.mkdir(download_path)
    file_path = download_diana_raw(mir, download_path)
    rows_data = []
    with open(file_path, 'r') as f:
        for row in f.readlines():
            row_data = parse_row(row)
            if row_data: rows_data.append(row_data)
    diana_raw = pd.DataFrame(rows_data)
    logging.info(l_DIANA)
    # Enrich Diana_raw
    enrich_df = get_trans_id_to_gene()
    # In the merging process there are a few genes that are lost. The reason
    # is that Diana uses Ensembl v.84, while the current version is higher, and
    # some transcripts were deprecated since.
    df = pd.merge(diana_raw, enrich_df, left_on=c_GENE, right_on=c_TRANS_ID)
    del df[c_GENE];
    del df[c_TRANS_ID];
    del df[c_GENE_ID]
    df = df.rename({'Gene name': c_GENE}, axis=1)
    return df


def get_mirdb_data(mir) -> pd.DataFrame:
    def parse_row(row):
        row_dict = {}
        row = row.text.split(NEW_ROW)
        if len(row) == GENE_TR_LINES_NUMBER:
            row_dict[c_GRADE] = row[1]
            data = row[2].split()
            row_dict[c_GENE] = data[1]
            row_dict[c_INFO] = ' '.join(data[2:])
        return row_dict

    def get_mir_raw_data(mir):
        DEBUG = os.environ['DEBUG'] != 'False'
        url = u_MIRDB
        driver, wait = launch_chrome(url, not DEBUG, wait_time=2)
        insert_box = driver.find_element_by_xpath(
            x_m_insert_box).send_keys(mir)
        submit = driver.find_element_by_xpath(x_m_submit).click()
        try:
            overload_warning = wait.until(
                EC.presence_of_element_located((By.XPATH,
                                                x_m_warning)))
            raise Exception(const.MIRDB_OVERLOAD_ERROR)
        except TimeoutException:
            pass
        results = long_wait(wait, x_m_get_results)
        results.click()
        rows = driver.find_elements_by_tag_name(TABLE_ROW_TAG)
        return rows

    df_rows = []
    rows = get_mir_raw_data(mir)
    for row in rows:
        row_data = parse_row(row)
        if row_data: df_rows.append(row_data)
    df = pd.DataFrame(df_rows)
    df[c_GRADE] = df[c_GRADE].astype(int)
    logging.info(l_MIRDB)
    return df


def get_trans_id_to_gene() -> pd.DataFrame:
    def download_mart(download_path, file_path):
        DEBUG = os.environ.get('DEBUG') != 'False'
        url = u_ENSAMBL
        # Deals with bad loading of url which required to restart the driver
        while True:
            driver, wait = launch_chrome(url, not DEBUG, wait_time=5,
                                         download_folder=download_path)
            try:
                get_results = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, x_e_get_results))).click()
                x_e_download_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, x_e_download))).click()
                break
            except TimeoutException:
                driver.quit()
                continue
        temp_file_name = wait_for_download_path(download_path)
        # Just uses to ignore the premmision Error that came up straight
        # after downloading the file for no reason
        while True:
            try:
                os.rename(temp_file_name, file_path)
                break
            except PermissionError:
                continue

    def parse_rows(file_path):
        data = []
        with open(file_path, 'r') as f:
            cols = f.readline().rstrip('\n').split(',')
            for row in f.readlines():
                row = row.rstrip('\n').split(',')
                row_data = {}
                for i, col in enumerate(cols):
                    # Removes the source of the phenotype
                    if col == c_GENE_DESCRIPTION:
                        source_comment_index = row[i].find(START_COMMENT)
                        if source_comment_index != NOT_FOUND_CHAR:
                            row_data[col] = row[i][:source_comment_index]
                            continue
                    row_data[col] = row[i]
                data.append(row_data)
        #  Removes the duplicate values (caused by phenotype description)
        df = pd.DataFrame(data).drop_duplicates(subset=[c_TRANS_ID])
        return df

    # TODO: add function that deletes old files
    download_path = os.path.join(os.getcwd(), f_data_tables_folder, p_ENSEMBL)
    file_path = os.path.join(download_path, p_MART_EXPORT_CSV)
    if not os.path.isfile(file_path):
        logging.info(l_ENSAMBL_DOWNLOAD)
        os.makedirs(download_path, exist_ok=True)
        download_mart(download_path, file_path)
    df = parse_rows(file_path)
    logging.info(l_TRANCE_ID_TO_GENE_NAME)
    return df


def get_gene_expression():
    exp_path = os.path.join(os.getcwd(), f_data_tables_folder,
                            p_GENE_EXPRESSION)
    exp_df = pd.read_csv(exp_path, sep='\t')
    exp_df = exp_df[~exp_df['Reliability'].isin(['Uncertain', np.nan])]
    exp_df = exp_df[exp_df['Level'] != 'Not representative']
    return exp_df


def new_search(key, key_type) -> str:
    def create_metadata(path):
        data = {}
        data[const.r_DATE_TIME] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        data[const.r_MIR_SEQ] = mir_seq
        data[const.r_MIR_NAME] = mir_name
        with open(os.path.join(path, p_META), 'w') as file:
            json.dump(data, file)

    logging.info(l_NEW_SEARCH)
    if key_type == MIR_SEQ_KEY:
        for i in key:
            if i not in const.MIR_CHARS:
                raise Exception(const.WRONG_MIR_ERROR)
        if len(key) > 30 or len(key) < 17:
            raise Exception(const.LENGTH_ERROR)
    mir_name = key if key_type == MIR_NAME_KEY else mir_seq_to_name(key)
    mir_seq = key if key_type == MIR_SEQ_KEY else mir_name_to_seq(key)
    if len(mir_seq) > 30 or len(mir_seq) < 17:
        raise Exception(const.LENGTH_ERROR)
    # search temp files folder
    rand = ''.join([str(randint(0, 9)) for num in range(0, 6)])
    temp_foler_name = os.path.join(f_history_folder, f'{mir_seq[-6:]}_{rand}')
    os.makedirs(temp_foler_name)
    diana_df = get_diana_data(mir_seq, temp_foler_name)
    mirdb_df = get_mirdb_data(mir_seq)
    # save files
    diana_df.to_csv(os.path.join(temp_foler_name, f_DIANA_CSV), index=False)
    mirdb_df.to_csv(os.path.join(temp_foler_name, f_MIRDB_CSV), index=False)
    create_metadata(temp_foler_name)
    return temp_foler_name


def mir_name_to_seq(mir_name) -> str:
    def get_mir_acc(mir_name):
        DEBUG = os.environ['DEBUG'] != 'False'
        url = u_MIRBASE
        driver, wait = launch_chrome(url, not DEBUG, wait_time=5)
        mir_name_entry = driver.find_element_by_xpath(x_MIR_NAME_ENTRY)
        mir_name_entry.send_keys(mir_name)
        mir_name_entry.send_keys(Keys.ENTER)
        try:
            mir_filter = wait.until(
                EC.element_to_be_clickable((By.XPATH,
                                            x_MIR_FILTER)))
        except TimeoutException:
            try:
                x = '//*[@id="accession"]'
                acc = driver.find_element_by_xpath(x).text
                return acc
            except:
                raise Exception(const.TEMP_UNKNOWN_ERROR)
        mir_filter.send_keys(HUMAN_MIR_PRE)
        results = driver.find_element_by_id(x_RESULTS_DIV_ID) \
            .find_elements_by_tag_name('tr')
        for row in results:
            # Filters the headline of the table
            row = row.text.split(' ')
            full_mir_name = row[0]
            if full_mir_name[:3] == HUMAN_MIR_PRE:
                return row[1]

    mir_acc = get_mir_acc(mir_name)
    if not mir_acc: raise Exception(const.MIR_NAME_NOT_FOUND_ERROR)
    url = u_MIRBASE_SEQ_QUERY + mir_acc
    req = requests.get(url)
    logging.info(l_MIR_NAME_TO_SEQ)
    return req.text.split('\n')[2]


def mir_seq_to_name(mir_seq) -> str:
    DEBUG = os.environ.get('DEBUG') != 'False'
    url = u_MIRBASE
    driver, wait = launch_chrome(url, not DEBUG, wait_time=2)
    mir_seq_entry = driver.find_element_by_xpath(x_MIR_SEQ_ENTRY)
    mir_seq_entry.send_keys(mir_seq)
    human_filter = driver.find_element_by_xpath(x_SEQ_HSA_FILTER).click()
    submit = driver.find_element_by_xpath(x_SEQ_ENTRY_SUBMIT).click()
    try:
        results = wait.until(
            EC.presence_of_element_located((By.XPATH,
                                            x_seq_results))). \
            find_elements_by_tag_name('tr')
        for row in results[1:]:  # Starts with [1:] to avoid the table title
            row = row.text.split(' ')
            if int(row[7]) >= 95:
                logging.info(l_mir_seq_to_name_success)
                return row[1]
    except TimeoutException:
        logging.info(l_mir_seq_to_name_fail)
        return ''


def fetch_data(key) -> dict:
    res = {const.s_SEARCH_NOVEL: True}
    # Filter input
    # Removes spaces from the end and the start of the input
    key = key.rstrip().lstrip()
    # Sanity check input type
    key_type = validate_search_key_type(key)
    if key_type == SEARCH_ID_KEY:
        try:
            folder_path = os.path.join(f_history_folder, key)
            diana_df = pd.read_csv(os.path.join(folder_path, f_DIANA_CSV))
            mirdb_df = pd.read_csv(os.path.join(folder_path, f_MIRDB_CSV))
            res[const.s_SEARCH_PATH] = folder_path
            res[const.s_SEARCH_NOVEL] = False
        except FileNotFoundError:
            raise Exception(const.SEARCH_ID_NOT_FOUND_ERROR)
    elif key_type in [MIR_SEQ_KEY, MIR_NAME_KEY]:
        res[const.s_SEARCH_PATH] = new_search(key, key_type)
    else:
        raise Exception(const.WRONG_SEARCH_KEY_FETCHED)
    return res


def get_results_data(search_folder, min_avg=None, min_grade=None,
                     tissue=None, tissue_level=None,
                     cell_type=None, cell_type_level=None) -> \
        dict:
    def read_metadata(path):
        with open(os.path.join(path, p_META), 'r') as f:
            meta_data = json.load(f)
        return meta_data

    mirdb_df = pd.read_csv(os.path.join(search_folder, f_MIRDB_CSV))
    diana_df = pd.read_csv(os.path.join(search_folder, f_DIANA_CSV))
    mirdb_df[c_REL_GRADE] = mirdb_df.index + 1
    diana_df[c_REL_GRADE] = diana_df.index + 1
    if min_grade:
        mirdb_df = mirdb_df[mirdb_df[c_GRADE] > min_grade]
        diana_df = diana_df[diana_df[c_GRADE] > min_grade]
    # Checks for merge
    df_merge = pd.merge(diana_df, mirdb_df, on=[c_GENE])
    df_merge = df_merge.rename(
        columns={c_GRADE + '_x': c_GRADE_D, c_GRADE + '_y':
            c_GRADE_M, c_REL_GRADE + '_x': c_REL_GRADE_D,
                 c_REL_GRADE + '_y': c_REL_GRADE_M})
    df_merge[c_GRADE_AVG] = (df_merge[c_GRADE_M] + df_merge[c_GRADE_D]) / 2
    if min_avg:
        df_merge = df_merge[df_merge[c_GRADE_AVG] > min_avg]
    df_merge[c_REL_GRADE_AVG] = (df_merge[c_REL_GRADE_D] + df_merge[
        c_REL_GRADE_M]) / 2
    df_merge.sort_values(by=[c_REL_GRADE_AVG], inplace=True,
                         ascending=True)
    df_merge.reset_index(inplace=True)
    # Gene Expression Merge
    exp_df = get_gene_expression()
    df_merge = pd.merge(df_merge, exp_df, how='left', left_on='gene',
                        right_on='Gene name')
    # Gene Expression filters data
    s_tissue = list(df_merge[c_exp_tissue].dropna().unique())
    s_cell_type = list(df_merge[c_EXP_CELL_TYPE].dropna().unique())
    s_level = list(df_merge[c_EXP_LEVEL].dropna().unique())
    # Filter
    if tissue:
        # TODO: add scale instead of exact value
        df_merge = df_merge[(df_merge[c_exp_tissue] == tissue) &
                            (df_merge[c_EXP_LEVEL].
                             isin(get_higher_levels(tissue_level)))]
    if cell_type:
        # TODO: add scale instead of exact value
        df_merge = df_merge[(df_merge[c_EXP_CELL_TYPE] == cell_type) &
                            (df_merge[c_EXP_LEVEL].
                             isin(get_higher_levels(cell_type_level)))]
    short_display = df_merge[[c_GENE, c_GRADE_D, c_REL_GRADE_D, c_GRADE_M,
                              c_REL_GRADE_M, c_GRADE_AVG,
                              c_REL_GRADE_AVG]].drop_duplicates()
    df_merge = df_merge[[c_GENE, c_GRADE_D, c_REL_GRADE_D, c_GRADE_M,
                         c_REL_GRADE_M, c_GRADE_AVG, c_REL_GRADE_AVG, c_INFO,
                         c_GENE_DESCRIPTION, c_PHENO_DESCRIPTION]]
    if 'index' in df_merge: del df_merge['index']
    results_data = {const.r_STATS: [('Diana', len(diana_df)), ('MirDB',
                                                               len(mirdb_df)),
                                    ('Both', len(short_display))],
                    const.r_GENES: list(zip(short_display['gene'].values,
                                            short_display[
                                                c_GRADE_AVG].values)),
                    const.r_DATA: df_merge,
                    const.r_FILTER: {const.r_TISSUE: tissue,
                                     const.r_TISSUE_LEVEL: tissue_level,
                                     const.r_CELL_TYPE: cell_type,
                                     const.r_CELL_TYPE_LEVEL:
                                         cell_type_level,
                                     const.r_MIN_GRADE: min_grade,
                                     const.r_MIN_AVG: min_avg},
                    const.r_SELECTIONS: {const.r_TISSUE: s_tissue,
                                         const.r_CELL_TYPE: s_cell_type,
                                         const.r_LEVEL: s_level}}
    logging.info(l_results_data_served)
    return {**results_data, **read_metadata(search_folder)}


def open_search_folder():
    if not os.path.isdir(f_history_folder):
        os.makedirs(f_history_folder)
    os.system(f"start {f_history_folder}")


def open_readme():
    os.system(f"start README.txt")


def open_results(data, path):
    file_path = os.path.join(path, 'mir_results.csv')
    data.to_csv(file_path, index=False)
    os.system(f"start EXCEL.EXE {file_path}")


if __name__ == '__main__':
    new_search('CAAGCUUGUAUCUAUAGGUAUG', MIR_SEQ_KEY)
