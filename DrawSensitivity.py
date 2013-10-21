#!/usr/bin/env python
# ==============================================================================
# ==============================================================================
# = example usage:
# =   python DrawSensitivity.py sensitivity.txt
# ==============================================================================

import sys
import os.path
import optparse
import time
import array

import ROOT
# import rootlogon
# import metaroot

# ------------------------------------------------------------------------------
def readFile(file):
    x_title = 'x'
    y_title = 'y'
    x = []
    y = []
    z = []

    f = open(file)
    for l in map(lambda x: x.rstrip('\n'), f.readlines()):
        if l[0] == '#': continue
        if 'x:' in l:
            print 'found x title'
            x_title = l.split(':')[1]
            continue
        if 'y:' in l:
            print 'found y title'
            y_title = l.split(':')[1]
            continue

        data = l.split()
        print data

        x.append(float(data[0]))
        y.append(float(data[1]))
        z.append(float(data[2]))

    return {'x_title':x_title, 'y_title':y_title, 'x':x, 'y':y, 'z':z}

# ------------------------------------------------------------------------------
def plotContour(x, y, z, x_title = 'x', y_title = 'y'):
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    sig_graph = ROOT.TGraph2D( 'h_sig_map'
                             , 'significance'
                             , len(x)
                             , array.array('d', x)
                             , array.array('d', y)
                             , array.array('d', z)
                             )

    sig_graph.SetMinimum(0)
    sig_graph.SetMaximum(2)

    # # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # contour_levels = [1.64]
    # contour_lines = getContourLines( sig_graph
    #                                , contour_levels
    #                                , [2]*len(contour_levels)
    #                                )
    # # for cl in contour_lines:
    # #     cl.Draw('SAME')

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    points = ROOT.TGraph( len(x)
                        , array.array('d', x)
                        , array.array('d', y)
                        )
    points.SetMarkerStyle(20)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    c_sig = ROOT.TCanvas('c_sig', 'sig', 600, 600)
    c_sig.SetLeftMargin( 0.15)
    c_sig.SetRightMargin(0.15)

    sig_graph.GetXaxis().SetTitle(x_title)
    sig_graph.GetYaxis().SetTitle(y_title)
    sig_graph.GetZaxis().SetTitle('Z_{N}')

    sig_graph.GetXaxis().SetTitleOffset(1.1)
    sig_graph.GetYaxis().SetTitleOffset(1.5)

    sig_graph.Draw('COLZ')
    points.Draw('PSAME')

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    contour_levels = [0.5, 1.64]
    contour_dict = getContourLines( sig_graph
                                  , contour_levels
                                  , [2]*len(contour_levels)
                                  )
    contour_lines = contour_dict['contours']
    for i, cl in enumerate(contour_lines):
        cl.Draw('LSAME')

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    return {'graph':sig_graph, 'canv':c_sig, 'points':points}

# ------------------------------------------------------------------------------
def getContourLines( plot
                   , contour_levels = [0.05]
                   , contour_colors = [1]
                   ):
    """
    Given a 2D plot, find and return the contour lines corresponding to the
    levels listed in contour_levels
    """
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # check type of plot and get temp histogram
    if isinstance(plot, ROOT.TH2):
        h = plot.Clone('hist_temp')
    elif isinstance(plot, ROOT.TGraph2D):
        h = plot.GetHistogram().Clone('hist_temp')
        # h = plot.GetHistogram()

    # add contour levels to temp histogram
    h.SetContour( len(contour_levels)
                , array.array('d', contour_levels)
                )

    # draw temp histogram to canvas and update to get contours
    c = ROOT.TCanvas('c_temp')
    h.Draw('CONT Z LIST')
    c.Update()

    # list to store the contour graphs which are created and will be returned
    list_of_contour_graphs = []
    contours = ROOT.gROOT.GetListOfSpecials().FindObject('contours')
    for i in xrange(contours.GetSize()):
        this_contour = contours.At(i)
        for j in xrange(this_contour.GetSize()):
            curve = this_contour.At(j)
            cv = curve.Clone('%s_cv_%d_%d' % (plot.GetName(),i,j))

            cv.SetLineColor(contour_colors[i])
            cv.SetLineWidth(3)

            list_of_contour_graphs.append(cv)
    c.Close()
    return {'contours':list_of_contour_graphs, 'hist':h}

# ==============================================================================
if __name__ == '__main__':
    config_file = sys.argv[1]
    print config_file
    # data = readFile('sensitivity.txt')
    data = readFile(config_file)
    sig = plotContour( data['x']
                     , data['y']
                     , data['z']
                     , data['x_title']
                     , data['y_title']
                     )

    sig['canv'].Print('sig.pdf')

