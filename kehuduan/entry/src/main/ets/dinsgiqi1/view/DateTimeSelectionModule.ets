/*
 * Copyright (c) 2024 Huawei Device Co., Ltd.
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

import { DataSource, Data } from '../viewmodel/DateTimeSelectionModuleData';
import { LoadingStatus } from '../common/CommonEnums';
import { LoadingFailedView } from '../view/LoadingFailedView';

import { BreakpointConstants } from '../common/BreakpointConstants';
import { BreakpointType } from '../util/BreakpointType';
import LazyDataSource from '../util/LazyDataSource';
import { CommonConstants } from '../common/CommonConstants';
import { ModuleTitleComponent } from '../common/ModuleTitleComponent'

@Component
export struct DateTimeSelectionModule {
  @State itemModel: Data =
    Data.getInstance();
  @Prop listDirection: Axis = Axis.Horizontal
  @State moduleTitle: string = "定时任务管理";
  @State moduleRedirectContent: string = "查看更多";
  @State loadingStatus: LoadingStatus = LoadingStatus.OFF;
  @State lazyDataSource: LazyDataSource<DataSource> =
    this.itemModel.lazyDataSource;
  private spaceArray: string[] = ['8vp', '16vp', '20vp'];
  @Consume('appPathStack') appPathStack: NavPathStack;
  @StorageLink('currentWidthBreakpoint') currentWidthBreakpoint: string = BreakpointConstants.BREAKPOINT_SM;

  jump(): void {
    this.appPathStack.pushPathByName('EmptyPagePathStack', null);
  }

  aboutToAppear() {
    this.loadResources();

  }

  loadResources(): void {
    this.loadingStatus = LoadingStatus.LOADING;
    this.itemModel.getResources().then(() => {
      this.loadingStatus = LoadingStatus.SUCCESS;
    }).catch(() => {
      this.loadingStatus = LoadingStatus.FAILED;
    });
  }

  build() {
    Column() {
      ModuleTitleComponent({ title: this.moduleTitle, moduleRedirectContent: this.moduleRedirectContent })

      if (this.loadingStatus === LoadingStatus.FAILED) {
        LoadingFailedView(() => this.loadResources())
      }
      if (this.loadingStatus === LoadingStatus.SUCCESS) {
        List({
          space: new BreakpointType(this.spaceArray[0], this.spaceArray[1],
            this.spaceArray[2]).getValue(this.currentWidthBreakpoint)
        }) {
          LazyForEach(this.lazyDataSource, (item: DataSource) => {
            ListItem() {
              HorizontalGraphicTextFunctionItem2({
                icon: item.getIcon(),
                title: item.getTitle(),
                description: item.getDescription()
              })
            }
            .width('150vp')
            .height('60vp')
            .onClick(() => {
              this.jump()
            })
            .borderRadius($r('sys.float.corner_radius_level4'))
            .backgroundColor($r('app.color.comp_background_primary_trans'))
          }, (item: DataSource, index: number) => index + JSON.stringify(item))
        }
        .width('auto')
        .height('auto')
        .listDirection(this.listDirection)
        .scrollBar(BarState.Off)
      }
    }
    .width('92%')
    .margin({ bottom: "10vp" })
  }
}


@Component
export struct HorizontalGraphicTextFunctionItem2 {
  @State title: string = '模块名';
  @State description: string = '跳转';
  @State icon: Resource = $r("app.media.ic_public_app");

  build() {
    Row() {
      Column() {
        /**
         * TODO:
         * please modify it according to the actual situation.
         * directly modify {@link SwiperFlatten_HorizontalGraphicTextFunctionItem2Model#TITLES}
         * or refactor method {@code getResources()} to implement your custom code logic.
         * @see SwiperFlatten_HorizontalGraphicTextFunctionItem2Model#getResources()
         */
        Text(this.title)
          .margin({ bottom: '3vp' })
          .fontColor($r('app.color.font_primary'))
          .maxFontSize($r('app.integer.subtitle_text_M'))
          .minFontSize($r('app.integer.caption_text_L'))
          .fontWeight(FontWeight.Medium)
          .textOverflow({ overflow: TextOverflow.Ellipsis })
          .maxLines(1)
        /**
         * TODO:
         * please modify it according to the actual situation.
         * directly modify {@link SwiperFlatten_HorizontalGraphicTextFunctionItem2Model#DESCRIPTIONS}
         * or refactor method {@code getResources()} to implement your custom code logic.
         * @see SwiperFlatten_HorizontalGraphicTextFunctionItem2Model#getResources()
         */
        Text(this.description)
          .fontColor($r('app.color.font_secondary'))
          .maxFontSize($r('app.integer.body_text_S'))
          .minFontSize($r('app.integer.caption_text_M'))
          .fontWeight(FontWeight.Regular)
          .textOverflow({ overflow: TextOverflow.Ellipsis })
          .maxLines(1)
      }
      .width('50%')
      .layoutWeight(1)
      .alignItems(HorizontalAlign.Start)
      .padding({ left: 6, right: 2 })

      /**
       * TODO:
       * please modify it according to the actual situation.
       * directly modify {@link SwiperFlatten_HorizontalGraphicTextFunctionItem2Model#ICONS}
       * or refactor method {@code getResources()} to implement your custom code logic.
       * @see SwiperFlatten_HorizontalGraphicTextFunctionItem2Model#getResources()
       */
      Column() {
        Image(this.icon)
          .height('60%')
          .constraintSize({ maxWidth: '100%' })
          .objectFit(ImageFit.Contain)
      }
      .width('30%')
      .margin({ right: 2 })
      .alignItems(HorizontalAlign.End)
    }
    .justifyContent(FlexAlign.SpaceBetween)
    .borderRadius($r('sys.float.corner_radius_level8'))
    .width(CommonConstants.FULL_PERCENT)
    .height(CommonConstants.FULL_PERCENT)
  }
}
