#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging.config
import pathlib
from typing import List

import matplotlib.pyplot as plt

import common.Calibrator.calibrator_conf as calibrator_conf
from common.PerformanceDatastructs.perf_datastruct import Perf
from common.environment_variable import load_server_logging_conf_file

load_server_logging_conf_file()


class TwoDimensionsPlot:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    # ========================= EXTERNAL USAGE =========================

    def print_graph(self, perf_list: List[Perf], output_path: pathlib.Path, file_name: str = "overview.png"):
        # Print a graph with the TPR,TNR,FPR,FNR ... on one unique chart

        output_file = output_path / file_name
        self.logger.debug(f"Computing and saving graph with threshold at {output_file}")

        plt.clf()
        legend = self.plot_perf_list(perf_list)
        self.add_meta(legend)
        self.save_fig(output_path=output_file)

    def print_graph_with_thresholds(self, perf_list: List[Perf], thresholds_handler: calibrator_conf.Default_calibrator_conf, output_path: pathlib.Path,
                                    file_name: str = "overview_with_thresholds.png"):
        # Print a graph with the TPR,TNR,FPR,FNR ... with thresholds provided on one unique chart

        output_file = output_path / file_name
        self.logger.debug(f"Computing and saving graph with threshold at {output_file}")

        plt.clf()
        legend = self.plot_perf_list(perf_list)
        legend += self.plot_thresholds(thresholds_handler)
        self.add_meta(legend)

        self.save_fig(output_path=output_file)

    # ========================= INTERNAL (FACTORIZATION PURPOSES) =========================
    def plot_perf_list(self, perf_list: List[Perf]):
        self.logger.info(perf_list)

        TPR_list = [p.score.TPR for p in perf_list]
        TNR_list = [p.score.TNR for p in perf_list]
        FNR_list = [p.score.FNR for p in perf_list]
        FPR_list = [p.score.FPR for p in perf_list]
        ACC_list = [p.score.ACC for p in perf_list]
        F1_list = [p.score.F1 for p in perf_list]
        threshold_list = [p.threshold for p in perf_list]

        self.logger.info(f"Perf List : {perf_list}")
        self.logger.info(f"ACC List : {ACC_list}")
        self.logger.info(f"Thresholds List : {threshold_list}")

        # order :  absciss followed by ordinates
        plt.plot(threshold_list, ACC_list)
        plt.plot(threshold_list, TPR_list)
        plt.plot(threshold_list, TNR_list)
        plt.plot(threshold_list, FNR_list)
        plt.plot(threshold_list, FPR_list)
        plt.plot(threshold_list, F1_list)

        legend = ('Accuracy', 'True Positive Rate', 'True Negative Rate', 'False Negative rate', 'False Positive rate', 'F1')
        return legend

    @staticmethod
    def add_meta(legend):

        plt.legend(legend, loc='upper right')
        plt.xlabel("Threshold values [0-1]")
        plt.ylabel("Indicator value [0-1]")
        plt.title("Performance measure depending on threshold for cluster creation")

    def plot_thresholds(self, thresholds_handler: calibrator_conf.Default_calibrator_conf):
        self.logger.info(thresholds_handler)

        # x coordinates for the lines
        xcoords = []
        # colors for the lines
        colors = []
        # Labels
        labels = []

        if thresholds_handler.thre_upper_at_least_xpercent_TPR is not None:
            xcoords.append(thresholds_handler.thre_upper_at_least_xpercent_TPR)
            colors.append('b')
            labels.append('TPR/Maybe to No ' + str(thresholds_handler.thre_upper_at_least_xpercent_TPR))
        if thresholds_handler.thre_upper_at_most_xpercent_FNR is not None:
            xcoords.append(thresholds_handler.thre_upper_at_most_xpercent_FNR)
            colors.append('g')
            labels.append('FNR/Maybe to No ' + str(thresholds_handler.thre_upper_at_most_xpercent_FNR))
        if thresholds_handler.maximum_F1 is not None:
            xcoords.append(thresholds_handler.maximum_F1)
            colors.append('y')
            labels.append('F1')
        if thresholds_handler.thre_below_at_least_xpercent_TNR is not None:
            xcoords.append(thresholds_handler.thre_below_at_least_xpercent_TNR)
            colors.append('r')
            labels.append('TNR/Yes to Maybe ' + str(thresholds_handler.thre_below_at_least_xpercent_TNR))
        if thresholds_handler.thre_below_at_most_xpercent_FPR is not None:
            xcoords.append(thresholds_handler.thre_below_at_most_xpercent_FPR)
            colors.append('m')
            labels.append('FPR/Yes to Maybe ' + str(thresholds_handler.thre_below_at_most_xpercent_FPR))

        for xc, l, c in zip(xcoords, labels, colors):
            plt.axvline(x=xc, label=l, linestyle='dashed', c=c)

        legend = tuple(labels)
        return legend

    def save_fig(self, output_path: pathlib.Path):
        # plt.show()
        plt.savefig(output_path, figsize=(15, 15), dpi=200)
        plt.clf()
        plt.cla()
        plt.close()