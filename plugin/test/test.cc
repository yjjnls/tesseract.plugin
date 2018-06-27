/*
 * Copyright 2018 KEDACOM Inc. All rights reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <tesseract/baseapi.h>
#include <leptonica/allheaders.h>
#include <assert.h>
int main(int argc, char *argv[])
{
    char *outText;

    tesseract::TessBaseAPI *api = new tesseract::TessBaseAPI();
    // Initialize tesseract-ocr with English, without specifying tessdata path
    if (api->Init(NULL, "eng")) {
        fprintf(stderr, "Could not initialize tesseract.\n");
        exit(1);
    }

    // Open input image with leptonica library
    Pix *image = NULL;
    if (argc <= 1)
        image = pixRead("test.bmp");
    else
        image = pixRead(argv[1]);
    api->SetImage(image);
    // Get OCR result
    outText = api->GetUTF8Text();
    char target[] = "0:00:05.233";
    printf("*************************************\n");
    printf("target:\t\t%s\nOCR output:\t%s", target, outText);
    printf("*************************************\n");
    int res = strncmp(outText, target, strlen(target));
    if (res != 0) {
        printf("OCR result is wrong!\n\n");
        throw "OCR result is wrong!";
    }

    // Destroy used object and release memory
    api->End();
    delete[] outText;
    pixDestroy(&image);

    return 0;
}
