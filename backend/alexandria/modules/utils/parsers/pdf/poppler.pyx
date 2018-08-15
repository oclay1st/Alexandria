# -*- coding: utf-8 -*-
from unicodedata import normalize, category
from cpython cimport bool as PyBool
from math import ceil

ctypedef bool GBool
DEF PRECISION=1e-6

cdef extern from "GlobalParams.h":
    GlobalParams *globalParams
    cdef cppclass GlobalParams:
        GBool getOverprintPreview()
        # GBool getOverprintPreview()
        # we need to init globalParams - just one during program run
globalParams = new GlobalParams()



cdef extern from "goo/GooString.h":
    cdef cppclass GooString:
        GooString(const char *sA)
        int getLength()
        char *getCString()
        GBool *hasUnicodeMarker()
        char getChar(int i)

cdef extern from "OutputDev.h":
    cdef cppclass OutputDev:
        pass

cdef extern from 'Annot.h':
    cdef cppclass Annot:
        pass

cdef extern from 'Page.h':
    cdef cppclass PDFRectangle:
        double x1, y1, x2, y2
    cdef cppclass Page:
        GooString *getText(double x1, double y1, double x2, double y2)
        int getNum()
        PDFRectangle *getCropBox()

cdef extern from 'Dict.h':
    cdef cppclass Dict:
        char *getKey(int n)
        int getLength()
        Object *lookup(char *key, Object *obj, int recursion)

cdef extern from 'Object.h':
    cdef cppclass Object:
        Dict *getDict()
        GooString *getString()
        GBool *isString()
        GBool *isDict()

cdef extern from "PDFDoc.h":
    cdef cppclass PDFDoc:
        double getPageMediaWidth(int page)
        double getPageMediaHeight(int page)
        int getPageRotate(int page)
        GBool isOk()
        int getNumPages()
        void displayPage(OutputDev *out, int page,
                         double hDPI, double vDPI, int rotate,
                         GBool useMediaBox, GBool crop, GBool printing,
                         GBool (*abortCheckCbk)(void *data) = NULL,
                         void *abortCheckCbkData = NULL,
                         GBool (*annotDisplayDecideCbk)(Annot *annot, void *user_data) = NULL,
                         void *annotDisplayDecideCbkData = NULL, GBool copyXRef = False)
        Object *getDocInfo(Object *info)
        Page *getPage(int page)
        void displayPageSlice(OutputDev *out, int page,
                              double hDPI, double vDPI, int rotate,
                              GBool useMediaBox, GBool crop, GBool printing,
                              int sliceX, int sliceY, int sliceW, int sliceH,
                              GBool (*abortCheckCbk)(void *data) = NULL,
                              void *abortCheckCbkData = NULL,
                              GBool (*annotDisplayDecideCbk)(Annot *annot, void *user_data) = NULL,
                              void *annotDisplayDecideCbkData = NULL, GBool copyXRef = False)


cdef extern from "PDFDocFactory.h":
    cdef cppclass PDFDocFactory:
        PDFDocFactory()
        PDFDoc *createPDFDoc(const GooString & uri, GooString *ownerPassword = NULL,
                             GooString *userPassword = NULL, void *guiDataA = NULL)

cdef extern from "TextOutputDev.h":
    cdef cppclass TextOutputDev:
        TextOutputDev(char *fileName, GBool physLayoutA,
                      double fixedPitchA, GBool rawOrderA, GBool append)
        TextPage *takeText()
        GooString *getText(double xMin, double yMin, double xMax, double yMax);

    cdef cppclass TextPage:
        void decRefCnt()
        TextFlow *getFlows()

    cdef cppclass TextFlow:
        TextFlow *getNext()
        TextBlock *getBlocks()

    cdef cppclass TextBlock:
        TextBlock *getNext()
        TextLine *getLines()
        void getBBox(double *xMinA, double *yMinA, double *xMaxA, double *yMaxA)

    cdef cppclass TextLine:
        TextWord *getWords()
        TextLine *getNext()

    cdef cppclass TextWord:
        TextWord *getNext()
        int getLength()
        GooString *getText()
        void getBBox(double *xMinA, double *yMinA, double *xMaxA, double *yMaxA)
        void getCharBBox(int charIdx, double *xMinA, double *yMinA,
                         double *xMaxA, double *yMaxA)
        GBool hasSpaceAfter()

cdef extern from 'CharTypes.h':
    ctypedef unsigned int Unicode;

cdef extern from "UTF.h":
    int TextStringToUCS4(GooString *textStr, Unicode ** ucs4)

"""
Classes for thumbnail generation
"""


cdef extern from 'splash/SplashTypes.h':
    cdef enum SplashImageFileFormat:
        splashFormatJpeg, splashFormatPng

    cdef enum SplashColorMode:
        splashModeRGB8,

    cdef enum SplashThinLineMode:
        splashThinLineDefault

    ctypedef unsigned char Guchar;
    ctypedef int SplashError;
    ctypedef Guchar SplashColor[3];

cdef extern from 'splash/SplashBitmap.h':
    cdef cppclass SplashBitmap:
        SplashError writeImgFile(SplashImageFileFormat format,
                                 char *fileName,
                                 int hDPI,
                                 int vDPI,
                                 const char *compressionString = ""
                                 )

cdef extern from 'SplashOutputDev.h':
    cdef cppclass SplashOutputDev:
        SplashOutputDev(SplashColorMode colorModeA, int bitmapRowPadA,
                        GBool reverseVideoA, SplashColor paperColorA,
                        GBool bitmapTopDownA,
                        SplashThinLineMode thinLineMode,
                        GBool overprintPreviewA)
        SplashBitmap *getBitmap()
        void startDoc(PDFDoc *doc)


cdef double RESOLUTION = 72.0

cdef class Document:
    cdef:
        PDFDoc *_doc
        int _pg
        int _max_pages
        PyBool phys_layout
        double fixed_pitch

    cdef void render_page(self, int page_no, OutputDev *dev):
        self._doc.displayPage(dev, page_no, RESOLUTION, RESOLUTION, 0, True, False, False)

    def __cinit__(self, char *fname, int max_pages=0, PyBool phys_layout=False, double fixed_pitch=0):
        self._doc = PDFDocFactory().createPDFDoc(GooString(fname))
        self._pg = 0
        self._max_pages = max_pages
        self.phys_layout = phys_layout
        self.fixed_pitch = fixed_pitch

    def __dealloc__(self):
        if self._doc != NULL:
            del self._doc

    property num_pages:
        def __get__(self):
            return self._doc.getNumPages()

    property max_pages:
        def __get__(self):
            if self._max_pages and self._max_pages < self.num_pages:
                return self._max_pages
            return self.num_pages

    def get_metadata(self):
        """extract pdf metadata title,author,creation date """
        cdef Object info
        cdef Dict *_dict
        cdef Unicode *uu;
        cdef GooString *text;
        cdef Object obj
        cdef char *test
        meta = {}
        self._doc.getDocInfo(&info)
        if info.isDict():
            _dict = info.getDict()
            for i in xrange(_dict.getLength()):
                key = _dict.getKey(i)
                if _dict.lookup(key, &obj,0).isString():
                    text = obj.getString()
                    if str(key) in ['Title', 'Author']:
                        # : get unicode correctly
                        value, length = [], TextStringToUCS4(text, &uu)
                        for w in xrange(length):
                            ch = chr(uu[w]) if uu[w] <= 127 else unichr(uu[w])
                            value.append(ch)
                        meta[key] = u''.join(value)
                        #
                    else:
                        meta[key] = text.getCString()
        return meta

    def get_text(self, pages=None):
        """Get text inside boxes"""
        cdef TextOutputDev *dev
        cdef Page *page
        cdef PDFRectangle *rect
        cdef list page_text = []
        dev = new TextOutputDev(NULL, self.phys_layout, self.fixed_pitch, False, False)
        if pages is None:
            pages = self.max_pages
        for i in xrange(1, pages):
            rect = self._doc.getPage(i).getCropBox()
            self._doc.displayPage(<OutputDev*> dev, i, RESOLUTION, RESOLUTION, 0, True, False, False)
            page_text.append('\n' + dev.getText(rect.x1, rect.y1, rect.x2, rect.y2).getCString() + '\n')
        del dev
        return ''.join(page_text)

    def __resolution(self, scale_to_x, scale_to_y, page):
        pg_w = self._doc.getPageMediaWidth(page)
        pg_h = self._doc.getPageMediaHeight(page)
        x_resolution = (RESOLUTION * scale_to_x) / pg_w
        y_resolution = (RESOLUTION * scale_to_y) / pg_h
        pg_w *= (x_resolution / RESOLUTION)
        pg_h *= (y_resolution / RESOLUTION)

        if self._doc.getPageRotate(page) == 90 or self._doc.getPageRotate(page) == 270:
            pg_w, pg_h = pg_h, pg_w

        return pg_w, pg_h, x_resolution, y_resolution

    def get_image_format(self, img_format):
        if img_format == 'png':
            return splashFormatPng
        if img_format == 'jpeg':
            return splashFormatJpeg

    def generate_thumbnail(self, path, x_scale_to, y_scale_to, image_format, page=1):
        """get thumbnail from pdf"""
        cdef SplashOutputDev *splash;
        cdef SplashBitmap *bitmap;
        cdef char *image = path;
        cdef Guchar paper_color[3];
        paper_color = [255, 255, 255]
        splash = new SplashOutputDev(splashModeRGB8, 4, False, paper_color, True, splashThinLineDefault,
                                     globalParams.getOverprintPreview())
        splash.startDoc(self._doc)
        pg_w, pg_h, x_res, y_res = self.__resolution(x_scale_to, y_scale_to, page)
        x, y, w, h = 0, 0, int(ceil(pg_w)), int(ceil(pg_h))
        w = int(ceil(pg_w - x)) if x + w > pg_w else w
        h = int(ceil(pg_h - y)) if y + h > pg_h else h
        self._doc. (<OutputDev*> splash, 1, x_res, y_res, -0, True, False, False, x, y, w, h)
        bitmap = splash.getBitmap()
        bitmap.writeImgFile(self.get_image_format(image_format), image, x_res, y_res)
        del splash

    def __iter__(self):
        return self

    def get_page(self, int pg):
        return PDFPage(pg, self)

    def __next__(self):
        if self._pg >= self.max_pages:
            raise StopIteration()
        self._pg += 1
        return self.get_page(self._pg)

cdef class PDFPage:
    cdef:
        int page_no
        TextPage *page
        Document doc
        TextFlow *curr_flow

    def __cinit__(self, int page_no, Document doc):
        cdef TextOutputDev *dev
        self.page_no = page_no
        dev = new TextOutputDev(NULL, doc.phys_layout, doc.fixed_pitch, False, False)
        doc.render_page(page_no, <OutputDev*> dev)
        self.page = dev.takeText()
        del dev
        self.curr_flow = self.page.getFlows()
        self.doc = doc

    def __dealloc__(self):
        if self.page != NULL:
            self.page.decRefCnt()

    def __iter__(self):
        return self

    def __next__(self):
        cdef Flow flow
        if not self.curr_flow:
            raise StopIteration()
        flow = Flow(self)
        self.curr_flow = self.curr_flow.getNext()
        return flow

    property page_no:
        def __get__(self):
            return self.page_no

cdef class Flow:
    cdef:
        TextFlow *flow
        TextBlock *curr_block

    def __cinit__(self, PDFPage pg):
        self.flow = pg.curr_flow
        self.curr_block = self.flow.getBlocks()

    def __iter__(self):
        return self

    def __next__(self):
        cdef Block b
        if not self.curr_block:
            raise StopIteration()
        b = Block(self)
        self.curr_block = self.curr_block.getNext()
        return b

cdef class Block:
    cdef:
        TextBlock *block
        TextLine *curr_line

    def __cinit__(self, Flow flow):
        self.block = flow.curr_block
        self.curr_line = self.block.getLines()

    #TODO - do we need to delete blocks, lines ... or are they destroyed with page?
    #     def __dealloc__(self):
    #         if self.block != NULL:
    #             del self.block

    def __iter__(self):
        return self

    def __next__(self):
        cdef Line l
        if not self.curr_line:
            raise StopIteration()
        l = Line(self)
        self.curr_line = self.curr_line.getNext()
        return l

    property bbox:
        def __get__(self):
            cdef double x1, y1, x2, y2
            self.block.getBBox(&x1, &y1, &x2, &y2)
            return BBox(x1, y1, x2, y2)

cdef class BBox:
    cdef double x1, y1, x2, y2

    def __cinit__(self, double x1, double y1, double x2, double y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def as_tuple(self):
        return self.x1, self.y1, self.x2, self.y2

    def __getitem__(self, i):
        if i == 0:
            return self.x1
        elif i == 1:
            return self.y1
        elif i == 2:
            return self.x2
        elif i == 3:
            return self.y2
        raise IndexError()

    property x1:
        def __get__(self):
            return self.x1
        def __set__(self, double val):
            self.x1 = val

    property x2:
        def __get__(self):
            return self.x2
        def __set__(self, double val):
            self.x2 = val

    property y1:
        def __get__(self):
            return self.y1
        def __set__(self, double val):
            self.y1 = val

    property y2:
        def __get__(self):
            return self.y2
        def __set__(self, double val):
            self.y2 = val

cdef class Line:
    cdef:
        TextLine *line
        double x1, y1, x2, y2
        unicode _text
        list _bboxes


    def __cinit__(self, Block block):
        self.line = block.curr_line

    def __init__(self, Block block):
        self._text = u''  # text bytes
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self._bboxes = []
        self._get_text()
        # assert len(self._text) == len(self._bboxes)

    def _get_text(self):
        cdef:
            TextWord *w
            GooString *s
            double bx1, bx2, by1, by2
            list words = []
            int offset = 0, i, wlen
            BBox last_bbox

        w = self.line.getWords()
        while w:
            wlen = w.getLength()
            assert wlen > 0
            # gets bounding boxes for all characters
            # and font info
            for i in range(wlen):
                w.getCharBBox(i, &bx1, &by1, &bx2, &by2)
                last_bbox = BBox(bx1, by1, bx2, by2)
                # if previous word is space update it's right end
                if i == 0 and words and words[-1] == u' ':
                    self._bboxes[-1].x2 = last_bbox.x1
                self._bboxes.append(last_bbox)
                #and then text as UTF-8 bytes
            s = w.getText()
            bad_characters = ['So', 'Cf', 'Cn', 'Cc']
            word_aux = s.getCString().decode('UTF-8')
            word = u''.join((c for c in normalize('NFD', word_aux) if category(c) not in bad_characters))
            #print s.getCString(), w.getLength(), len(s.getCString())
            words.append(word)  # decoded to python unicode string
            del s
            # must have same ammount of bboxes and characters in word
            # assert len(words[-1]) == wlen
            #calculate line bbox
            w.getBBox(&bx1, &by1, &bx2, &by2)
            if bx1 < self.x1 or self.x1 == 0:
                self.x1 = bx1
            if by1 < self.y1 or self.y1 == 0:
                self.y1 = by1
            if bx2 > self.x2:
                self.x2 = bx2
            if by2 > self.y2:
                self.y2 = by2
                # add space after word if necessary
            # if w.hasSpaceAfter():
            words.append(u' ')
            self._bboxes.append(BBox(last_bbox.x2, last_bbox.y1, last_bbox.x2, last_bbox.y2))
            w = w.getNext()
        self._text = u''.join(words)

    property bbox:
        def __get__(self):
            return BBox(self.x1, self.y1, self.x2, self.y2)

    property text:
        def __get__(self):
            return self._text

    property char_bboxes:
        def __get__(self):
            return self._bboxes
