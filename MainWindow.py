##    Copyright (C) 2011 Oleg Kertanov <okertanov@gmail.com>
##    All rights reserved.

from PyQt4 import QtCore, QtGui
import os
import socket
import logging
import inspect
import MainWindow_rc
import GitLib

#
# MainWindow class
#
class MainWindow(QtGui.QMainWindow, GitLib.GitLibDelegate) :
    def __init__(self):
        super(MainWindow, self).__init__()

        self.git = None
        self.settings = None
        self.projects = []

        self.InitPreferences()
        self.InitGitWorker()
        self.InitSignals()
        self.InitGit()
        self.InitUI()

    #
    # MainWindowGitDelegate methods
    #
    def GetLoggingEnabled(self):
        loglevel = logging.DEBUG
        return (True, loglevel, None, MainWindow.MainWindowLoggingHandler(logging.INFO, self))
    def GetTopDir(self):
        return os.path.expanduser('../')
    def Process(self, event = None, data = None):
        pass
    def OnScanItem(self, item = None):
        self.projects.append(item)
    def OnScanDone(self):
        self.emit(QtCore.SIGNAL("OnProjListItemsDone"), ())

    #
    # MainWindow methods
    #
    def InitPreferences(self):
        self.settings = QtCore.QSettings(GitLib.GITLIBAPPNAME + '.ini', QtCore.QSettings.IniFormat)
        self.settings.setValue("Geometry", self.saveGeometry())

    def InitGitWorker(self):
        self.worker = GitLib.GitWorker();
        self.worker.execute() #dry run

    def InitSignals(self):
        self.connect(self, QtCore.SIGNAL("OnProjListItemsDone"), self.OnProjListItemsDone)

    def InitGit(self):
        self.git = GitLib.GitLib(self)
        self.git.SetupGit();
        self.git.Version()

    def InitUI(self):
        self.CreateActions()
        self.CreateToolBar()
        self.CreateStatusBar()

        self.projGroupBox      = self.CreateLeftPane()
        self.gitCtxGroupBox    = self.CreateRightUpPane()
        self.gitTreeGroupBox   = self.CreateRightCenterPane()
        self.logGroupBox       = self.CreateRightDownPane()

        frame = QtGui.QFrame()
        mainLayout = QtGui.QGridLayout(frame)
        mainLayout.addWidget(self.projGroupBox,     0, 0, 0, 1)
        mainLayout.addWidget(self.gitCtxGroupBox,   0, 1)
        mainLayout.addWidget(self.gitTreeGroupBox,  1, 1)
        mainLayout.addWidget(self.logGroupBox,      2, 1)
        mainLayout.setColumnStretch(0, 15)
        mainLayout.setColumnStretch(1, 30)
        mainLayout.setRowStretch(0, 0)
        mainLayout.setRowStretch(1, 50)
        mainLayout.setRowStretch(2, 20)
        self.setCentralWidget(frame)

        self.setWindowTitle("Gitra-VCF [" + socket.gethostname() + "]")
        self.resize(940, 620)

    def ResetGitProjects(self):
        self.projects[:] = []
        self.listTree.hide()
        self.projList.clear()

    def ActivateGitProjects(self):
        self.listTree.show()
        self.projList.show()
        self.projList.setCurrentItem(self.projList.item(0))

    def AddGitProjectItem(self, item):
        qtItem = QtGui.QListWidgetItem(self.projList)
        qtItem.setText(item.name)
        qtItem.setData(QtCore.Qt.UserRole, item.path)
        qtItem.setData(QtCore.Qt.UserRole + 1, item)
        qtItem.setIcon(QtGui.QIcon(":/resources/giticonunknown.png"))

        self.listTree.show()

    def UiLogMessage(self, message):
        if hasattr(self, 'logEditor'):
            self.logEditor.moveCursor(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
            self.logEditor.insertHtml(message)
            self.logEditor.scrollToAnchor('')
        pass

    def CreateLeftPane(self):
        projList = self.projList = QtGui.QListWidget()
        projList.setViewMode(QtGui.QListView.ListMode)
        projList.setAcceptDrops(True)
        projList.setSpacing(2)
        projList.setIconSize(QtCore.QSize(48, 48))
        projList.currentItemChanged.connect(self.OnProjListItemChanged)

        projLayout = QtGui.QVBoxLayout()
        projLayout.addWidget(projList)

        groupBox = QtGui.QGroupBox("Projects")
        groupBox.setLayout(projLayout)

        return groupBox

    def CreateRightUpPane(self):
        gitBranchesCombo = QtGui.QComboBox();
        gitBranchesCombo.addItem("origin/master")
        gitBranchesCombo.addItem("origin/feature1")

        branchesLayout = QtGui.QHBoxLayout()
        branchesLayout.addWidget(QtGui.QLabel('Branches:'))
        branchesLayout.addWidget(gitBranchesCombo)

        gitTagsCombo = QtGui.QComboBox();
        gitTagsCombo.addItem("v1")
        gitTagsCombo.addItem("v2")
        gitTagsCombo.addItem("v3")

        tagsLayout = QtGui.QHBoxLayout()
        tagsLayout.addWidget(QtGui.QLabel('Tags:'))
        tagsLayout.addWidget(gitTagsCombo)

        gitRemotesCombo = QtGui.QComboBox();
        gitRemotesCombo.addItem("origin")
        gitRemotesCombo.addItem("upstream")

        remotesLayout = QtGui.QHBoxLayout()
        remotesLayout.addWidget(QtGui.QLabel('Remotes:'))
        remotesLayout.addWidget(gitRemotesCombo)

        cmdLayout = QtGui.QGridLayout()
        cmdLayout.addLayout (branchesLayout, 0, 1)
        cmdLayout.addLayout (tagsLayout, 0, 2)
        cmdLayout.addLayout (remotesLayout, 0, 3)
        cmdLayout.setRowStretch(3, 1)

        groupBox  = QtGui.QGroupBox("Context")
        groupBox.setLayout(cmdLayout)

        return groupBox

    def CreateRightCenterPane(self):
        treeModel = self.treeModel = QtGui.QDirModel()
        treeModel.setFilter(QtCore.QDir.Dirs    |
                    QtCore.QDir.NoDotAndDotDot  |
                    QtCore.QDir.NoSymLinks      |
                    QtCore.QDir.Files)

        listTree = self.listTree = QtGui.QTreeView()
        listTree.setRootIsDecorated(False)
        listTree.setIndentation(20)
        listTree.setSortingEnabled(True)
        listTree.setAlternatingRowColors(True)
        listTree.setModel(treeModel)
        listTree.setRootIndex(treeModel.index(QtCore.QDir.currentPath()));
        listTree.hide ()
        #listTree.setColumnCount(5)
        #listTree.setHeaderLabels(("Name", "Size", "Status", "Created", "Changed"))
        #listTree.header().setStretchLastSection(False)

        treeLayout = QtGui.QVBoxLayout()
        treeLayout.addWidget(listTree)

        groupBox = QtGui.QGroupBox("Tree")
        groupBox.setLayout(treeLayout)

        return groupBox

    def CreateRightDownPane(self):
        logEditor = self.logEditor = QtGui.QTextEdit()
        logEditor.setReadOnly(True)
        logEditor.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        logEditor.setPlainText("Starting...")
        logEditor.setHtml('<p><span style="color:darkblue">'
                          'git&gt;</span> # On branch <span style="color:darkred">master</span><br>'
                          '<span style="color:darkblue">'
                          'git&gt;</span> nothing to commit <span style="color:grey">(working directory clean)'
                          '</span><br></p>')

        logLayout = QtGui.QVBoxLayout()
        logLayout.addWidget(logEditor)

        groupBox = QtGui.QGroupBox("Log")
        groupBox.setLayout(logLayout)

        return groupBox

    def CreateToolBar(self):
        tbSize  = QtCore.QSize(36, 36)
        tbStyle = QtCore.Qt.ToolButtonTextUnderIcon

        self.fileToolBar = self.addToolBar("Main")
        self.fileToolBar.setIconSize(tbSize)
        self.fileToolBar.setToolButtonStyle(tbStyle)
        self.fileToolBar.addAction(self.RescanAction)
        self.fileToolBar.addAction(self.GitInitAction)
        self.fileToolBar.addAction(self.GitCloneAction)

        self.gitToolBar = self.addToolBar("GitInfo")
        self.gitToolBar.setIconSize(tbSize)
        self.gitToolBar.setToolButtonStyle(tbStyle)
        self.gitToolBar.addAction(self.GitStatusAction)
        self.gitToolBar.addAction(self.GitLogAction)
        self.gitToolBar.addAction(self.GitDiffAction)
        self.gitToolBar.addAction(self.GitConfigAction)

        self.gitAToolBar = self.addToolBar("GitAdvanced")
        self.gitAToolBar.setIconSize(tbSize)
        self.gitAToolBar.setToolButtonStyle(tbStyle)
        self.gitAToolBar.addAction(self.GitPullAction)
        self.gitAToolBar.addAction(self.GitFetchAction)
        self.gitAToolBar.addAction(self.GitCommitAction)
        self.gitAToolBar.addAction(self.GitPushAction)

        self.gitMToolBar = self.addToolBar("GitMerge")
        self.gitMToolBar.setIconSize(tbSize)
        self.gitMToolBar.setToolButtonStyle(tbStyle)
        self.gitMToolBar.addAction(self.GitBranchAction)
        self.gitMToolBar.addAction(self.GitTagAction)
        self.gitMToolBar.addAction(self.GitMergeAction)
        self.gitMToolBar.addAction(self.GitRebaseAction)

        self.helpToolBar = self.addToolBar("Help")
        self.helpToolBar.setIconSize(tbSize)
        self.helpToolBar.setToolButtonStyle(tbStyle)
        self.helpToolBar.addAction(self.HelpAction)
        self.helpToolBar.addAction(self.AboutAction)

    def CreateStatusBar(self):
        self.statusBar().showMessage("Ready")

    def CreateActions(self):
        self.RescanAction = QtGui.QAction(QtGui.QIcon(':/resources/rescan.png'), "&Rescan",
                self, shortcut="Ctrl+R", statusTip="Rescan the projects list",
                triggered=self.DoRescan)
        self.GitInitAction = QtGui.QAction(QtGui.QIcon(':/resources/gitinit.png'), "&Init",
                self, shortcut="Alt+2", statusTip="Create an empty git repository or reinitialize an existing one",
                triggered=self.DoGitInit)
        self.GitCloneAction = QtGui.QAction(QtGui.QIcon(':/resources/gitclone.png'), "&Clone",
                self, shortcut="Alt+1", statusTip="Clone a repository into a new directory",
                triggered=self.DoGitClone)
        self.GitStatusAction = QtGui.QAction(QtGui.QIcon(':/resources/gitstatus.png'), "&Status",
                self, shortcut="Alt+3", statusTip="Show the working tree status",
                triggered=self.DoGitStatus)
        self.GitLogAction = QtGui.QAction(QtGui.QIcon(':/resources/gitlog.png'), "&Log",
                self, shortcut="Alt+4", statusTip="Show commit logs",
                triggered=self.DoGitLog)
        self.GitDiffAction = QtGui.QAction(QtGui.QIcon(':/resources/gitdiff.png'), "&Diff",
                self, shortcut="Alt+5", statusTip="Show changes between commits, commit and working tree",
                triggered=self.DoGitDiff)
        self.GitConfigAction = QtGui.QAction(QtGui.QIcon(':/resources/gitconfig.png'), "&Config",
                self, shortcut="Alt+6", statusTip="Get and set repository or global options",
                triggered=self.DoGitConfig)

        self.GitPullAction = QtGui.QAction(QtGui.QIcon(':/resources/gitpull.png'), "&Pull",
                self, shortcut="Alt+7", statusTip="Fetch from and merge with another repository or a local branch",
                triggered=self.DoGitPull)
        self.GitFetchAction = QtGui.QAction(QtGui.QIcon(':/resources/gitfetch.png'), "&Fetch",
                self, shortcut="Alt+8", statusTip="Download objects and refs from another repository",
                triggered=self.DoGitFetch)
        self.GitCommitAction = QtGui.QAction(QtGui.QIcon(':/resources/gitcommit.png'), "&Commit",
                self, shortcut="Alt+9", statusTip="Record changes to the repository",
                triggered=self.DoGitCommit)
        self.GitPushAction = QtGui.QAction(QtGui.QIcon(':/resources/gitpush.png'), "&Push",
                self, shortcut="Alt+0", statusTip="Update remote refs along with associated objects",
                triggered=self.DoGitPush)

        self.GitBranchAction = QtGui.QAction(QtGui.QIcon(':/resources/gitbranch.png'), "&Branch",
                self, shortcut="Alt+Q", statusTip="List, create, or delete branches",
                triggered=self.DoGitBranch)
        self.GitTagAction = QtGui.QAction(QtGui.QIcon(':/resources/gittag.png'), "&Tag",
                self, shortcut="Alt+W", statusTip="Create, list, delete or verify a tag object",
                triggered=self.DoGitTag)
        self.GitMergeAction = QtGui.QAction(QtGui.QIcon(':/resources/gitmerge.png'), "&Merge",
                self, shortcut="Alt+E", statusTip="Join two or more development histories together",
                triggered=self.DoGitMerge)
        self.GitRebaseAction = QtGui.QAction(QtGui.QIcon(':/resources/gitrebase.png'), "&Rebase",
                self, shortcut="Alt+R", statusTip="Forward-port local commits to the updated upstream head",
                triggered=self.DoGitRebase)

        self.HelpAction = QtGui.QAction(QtGui.QIcon(':/resources/help.png'), "&Help",
                self, shortcut="Shift+?", statusTip="Gitra Help...",
                triggered=self.DoHelp)
        self.AboutAction = QtGui.QAction(QtGui.QIcon(':/resources/about.png'), "A&bout",
                self, shortcut="Ctrl+?", statusTip="About...",
                triggered=self.DoAbout)

    #Handlers
    def OnProjListItemChanged(self, current, previous):
        currentItem = self.projList.currentItem()
        if currentItem:
            itemsPath = currentItem.data(QtCore.Qt.UserRole).toString()
            if itemsPath:
                self.listTree.setRootIndex(self.treeModel.index(itemsPath));

    def OnProjListItemsDone(self):
        map(self.AddGitProjectItem, self.projects)
        self.ActivateGitProjects()

    #Events
    def showEvent(self, event):
        self.DoRescan()

    #Actions
    def DoRescan(self):
        self.ResetGitProjects()
        self.worker.enqueue(self.git.Scan)
        self.worker.execute()
        pass
    def DoGitClone(self):
        pass
    def DoGitInit(self):
        pass
    def DoGitStatus(self):
        pass
    def DoGitLog(self):
        pass
    def DoGitDiff(self):
        pass
    def DoGitConfig(self):
        pass
    def DoGitPull(self):
        pass
    def DoGitFetch(self):
        pass
    def DoGitCommit(self):
        pass
    def DoGitPush(self):
        pass
    def DoGitBranch(self):
        pass
    def DoGitTag(self):
        pass
    def DoGitMerge(self):
        pass
    def DoGitRebase(self):
        pass
    def DoHelp(self):
        pass
    def DoAbout(self):
        QtGui.QMessageBox.about(self, "About Gitra-VCF",
                "Gitra-VCF - version control frontend."
                "\n\n"
                "It's the projects aggregator with the Git support."
                "\n\n"
                "Copyright (C) 2011 Oleg Kertanov <okertanov@gmail.com>"
                "\n\n"
                "All rights reserved.")
        pass

    #
    # MainWindowLoggingHandler class
    #
    class MainWindowLoggingHandler(logging.Handler):
        def __init__(self, level, owner):
            logging.Handler.__init__(self, level)
            self.owner = owner
            pass
        def createLock(self):
            self.mutex = QtCore.QMutex()
            pass
        def acquire(self):
            self.mutex.lock()
            pass
        def release(self):
            self.mutex.unlock()
            pass
        def setLevel(self, level):
            self.level = level
            pass
        def filter(self, record):
            return record
            pass
        def flush(self):
            pass
        def close(self):
            pass
        def format(self, record):
            logleveldict = {}
            msg = record.getMessage()
            fmtmsgcolor  = 'DarkSlateGray'
            fmtloglevelcolor = 'SlateGray'
            fmtbody = '''<p><span style="color:%(loglevelcolor)s">'
                      %(loglevel)s&gt;&nbsp;</span>'
                      '<span style="color:%(msgcolor)s">%(message)s<span><br/></p>'''
            formatted = fmtbody % {'loglevelcolor':fmtloglevelcolor,
                                   'msgcolor':fmtmsgcolor,
                                   'loglevel':logging.getLevelName(record.levelno),
                                   'message':msg}
            return formatted
        def emit(self, record):
            self.owner.UiLogMessage(self.format(record))
            pass

