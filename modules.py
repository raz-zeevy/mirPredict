from launcher import launch_chrome, long_wait, wait_for_download_path
import os
from random import randint
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import const

# General
NOT_FOUND_CHAR = -1
NEW_ROW = "\n"
# file names
f_MIRDB_CSV = 'mirdb.csv'
f_DIANA_CSV = 'diana.csv'
f_searches_folder = 'searches_data'
# Ensembl
p_ENSEMBL = 'ensembl'
p_MART_EXPORT_CSV = 'mart_export.csv'
c_TRANS_ID = 'Transcript stable ID'
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
с_GRADE_AVG = 'Avg grade'
# XPATH's
x_d_accept_cookies = '/html/body/div[1]/div[6]/div[2]'
x_d_insert_box = '/html/body/div[1]/div[4]/div/div[2]/div/form/div[3]/textarea'
x_d_submit = '/html/body/div[1]/div[4]/div/div[2]/div/form/input'
x_d_download_results = '/html/body/div[1]/div[4]/div/div[3]/div/div/div/div[' \
                       '1]/div[4]/a'
x_m_insert_box = '/html/body/table[2]/tbody/tr/td[3]/form/table/tbody/tr[4]/td/textarea'
x_m_submit = '/html/body/table[2]/tbody/tr/td[3]/form/table/tbody/tr[5]/td/input[1]'
x_m_warning = '/html/body/table[2]/tbody/tr/td[3]/h2/font'
x_m_get_results = '/html/body/form/input[2]'
x_e_download = '/html/body/div[1]/div/div[3]/div[1]/div/form/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/div/table/tbody/tr/td/div[5]/table/tbody/tr[1]/td/div/table/tbody/tr[1]/td[2]/input[2]'
x_e_get_results = '/html/body/div[1]/div/div[3]/div[1]/div/form/table/tbody/tr[1]/td/div/table/tbody/tr/td[1]/a[3]'


def get_diana_data(mir, temp_foler_name):
    def download_diana_raw(mir, download_path):
        url = 'http://diana.imis.athena-innovation.gr/DianaTools/index.php?r' \
              '=mrmicrot/index'
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

    download_path = os.getcwd() + '\\' + temp_foler_name + "\dianaDB"
    os.mkdir(download_path)
    file_path = download_diana_raw(mir, download_path)
    rows_data = []
    with open(file_path, 'r') as f:
        for row in f.readlines():
            row_data = parse_row(row)
            if row_data: rows_data.append(row_data)
    diana_raw = pd.DataFrame(rows_data)
    # Enrich Diana_raw
    enrich_df = get_gene_enrich()
    # In the merging process there are a few genes that are lost. The reason
    # is that Diana uses Ensembl v.84, while the current version is higher, and
    # some transcripts were deprecated since.
    df = pd.merge(diana_raw, enrich_df, left_on=c_GENE, right_on=c_TRANS_ID)
    del df[c_GENE];
    del df[c_TRANS_ID]
    df = df.rename({'Gene name': c_GENE}, axis=1)
    return df


def get_mirdb_data(mir):
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
        url = 'http://mirdb.org/custom.html'
        driver, wait = launch_chrome(url, not DEBUG)
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
    return df


def get_gene_enrich():
    def download_mart(download_path, file_path):
        DEBUG = os.environ['DEBUG'] != 'False'
        url = 'http://www.ensembl.org/biomart/martview' \
              '/31db07defc7c705f4867eb4d985ab291?VIRTUALSCHEMANAME=default' \
              '&ATTRIBUTES=hsapiens_gene_ensembl.default.feature_page' \
              '.ensembl_transcript_id|hsapiens_gene_ensembl.default.feature_page' \
              '.external_gene_name|hsapiens_gene_ensembl.default.feature_page' \
              '.description|hsapiens_gene_ensembl.default.feature_page' \
              '.phenotype_description&FILTERS=&VISIBLEPANEL=resultspanel '
        # Deals with bad loading of url which required to restart the driver
        while True:
            driver, wait = launch_chrome(url, not DEBUG,
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
        os.rename(temp_file_name, file_path)

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
    download_path = os.path.join(os.getcwd(), p_ENSEMBL)
    file_path = os.path.join(download_path, p_MART_EXPORT_CSV)
    if not os.path.isfile(file_path):
        os.makedirs(download_path, exist_ok=True)
        download_mart(download_path, file_path)
    df = parse_rows(file_path)
    return df


def new_search(mir):
    if len(mir) > 30 or len(mir) < 17:
        raise Exception(const.LENGTH_ERROR)
    for i in mir:
        if i not in const.MIR_CHARS:
            raise Exception(const.WRONG_MIR_ERROR)
    # search temp files folder
    rand = ''.join([str(randint(0, 9)) for num in range(0, 6)])
    temp_foler_name = os.path.join(f_searches_folder, f'{mir[-6:]}_{rand}')
    os.mkdir(temp_foler_name)
    diana_df = get_diana_data(mir, temp_foler_name)
    mirdb_df = get_mirdb_data(mir)
    # save files
    diana_df.to_csv(os.path.join(temp_foler_name, f_DIANA_CSV), index=False)
    mirdb_df.to_csv(os.path.join(temp_foler_name, f_MIRDB_CSV), index=False)
    return diana_df, mirdb_df, temp_foler_name


def fetch_data(mir):
    DEBUG = os.environ['DEBUG']
    folder_path = os.path.join(f_searches_folder,DEBUG)
    if DEBUG == 'False':
        diana_df, mirdb_df, temp_folder_name = new_search(mir)
    elif DEBUG == '1':
        diana_df, mirdb_df, temp_folder_name = new_search(mir)
    else:
        diana_df = pd.read_csv(
            r"C:\Users\Raz_Z\Projects\Lab\mirPredict\{}\diana.csv"
            r"".format(folder_path))
        mirdb_df = pd.read_csv(r"C:\Users\Raz_Z\Projects\Lab\mirPredict"
                               r"\{}\mirdb.csv".format(folder_path))
    return diana_df, mirdb_df, folder_path


def get_results_data(data: tuple, min_avg=None,
                     min_grade=None):
    mirdb_df, diana_df = data[0], data[1]
    mirdb_df[c_REL_GRADE] = mirdb_df.index + 1
    diana_df[c_REL_GRADE] = diana_df.index + 1
    if min_grade:
        mirdb_df = mirdb_df[mirdb_df[c_GRADE] > min_grade]
        diana_df = diana_df[diana_df[c_GRADE] > min_grade]
    # Checks for merge
    merge = pd.merge(diana_df, mirdb_df, on=[c_GENE])
    merge = merge.rename(columns={c_GRADE+'_x': c_GRADE_D, c_GRADE+'_y':
        c_GRADE_M, c_REL_GRADE+'_x' : c_REL_GRADE_D,
        c_REL_GRADE+'_y': c_REL_GRADE_M})
    merge[с_GRADE_AVG] = (merge[c_GRADE_M] + merge[c_GRADE_D]) / 2
    if min_avg:
        merge = merge[merge[с_GRADE_AVG] > min_avg]
    merge[c_REL_GRADE_AVG] = (merge[c_REL_GRADE_D] + merge[c_REL_GRADE_M]) / 2
    merge.sort_values(by=[c_REL_GRADE_AVG], inplace=True,
                      ascending=True)
    merge.reset_index(inplace=True)
    short_display = merge[[c_GENE, c_GRADE_D, c_REL_GRADE_D, c_GRADE_M,
                           c_REL_GRADE_M, с_GRADE_AVG, c_REL_GRADE_AVG]]
    merge = merge[[c_GENE, c_GRADE_D, c_REL_GRADE_D, c_GRADE_M,
                   c_REL_GRADE_M, с_GRADE_AVG, c_REL_GRADE_AVG,c_INFO,
                   c_GENE_DESCRIPTION,c_PHENO_DESCRIPTION]]
    if 'index' in merge: del merge['index']
    return dict(stats=[('Diana', len(diana_df)), ('MirDB', len(mirdb_df)),
                       ('Both', len(merge))],
                genes=list(zip(short_display['gene'].values,
                               short_display[с_GRADE_AVG].values)),
                data=merge)


def open_results(data, path):
    file_path = os.path.join(path, 'mir_results.csv')
    data.to_csv(file_path, index=False)
    return file_path

