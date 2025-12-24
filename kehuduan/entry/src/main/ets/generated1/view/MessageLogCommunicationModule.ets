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


import { HorizontalListMessageItemModel } from '../viewmodel/MessageLogCommunicationModuleData'
import { List_HorizontalListMessageItemModel } from '../viewmodel/MessageLogCommunicationModuleData'
import { LoadingStatus } from '../common/CommonEnums';
import { LoadingFailedView } from '../view/LoadingFailedView';
import { ModuleTitleComponent } from '../common/ModuleTitleComponent';
import { BreakpointConstants } from '../common/BreakpointConstants';
import { BreakpointType } from '../util/BreakpointType';
import LazyDataSource from '../util/LazyDataSource';
import { CommonConstants } from '../common/CommonConstants'

@Component
export struct MessageLogCommunicationModule {
  @State itemModel: List_HorizontalListMessageItemModel =
    List_HorizontalListMessageItemModel.getInstance();
  @State moduleTitle: string = "消息日志";
  @State moduleRedirectContent: string = "查看更多";
  @State loadingStatus: LoadingStatus = LoadingStatus.OFF;
  @State lazyDataSource: LazyDataSource<HorizontalListMessageItemModel> =
    this.itemModel.lazyDataSource;
  private spaceArray: string[] = ['12vp', '16vp', '20vp'];
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
          LazyForEach(this.lazyDataSource, (item: HorizontalListMessageItemModel) => {
            ListItem() {
              HorizontalListMessageItem({
                title: item.getTitle(),
                avatar: item.getAvatar(),
                time: item.getTime(),
                content: item.getContent(),
                advertise: item.getAdvertise(),
              })
            }
            .height("60vp")
            .onClick(() => {
              this.jump()
            })
          }, (item: HorizontalListMessageItemModel, index: number) => index + JSON.stringify(item))
        }
        .width('auto')
        .height('auto')
        .divider({ "strokeWidth": 1 })
        .lanes(this.currentWidthBreakpoint === BreakpointConstants.BREAKPOINT_SM ? 1 : 2,
          "12vp")
        .listDirection(Axis.Vertical)
        .backgroundColor($r('app.color.comp_background_primary_trans'))
        .borderRadius($r('sys.float.corner_radius_level4'))
      }
    }
    .width('92%')
    .margin({ bottom: "10vp" })
    .padding({ bottom: 6 })
  }
}

@Component
export struct HorizontalListMessageItem {
  @State title: string = "消息号动态"
  @State avatar: Resource = $r('app.media.icon')
  @State time: string = "07:21"
  @State content: string = "[54条]携程全球购：海内曼澳门免税店到店购买还有三四五六七八折demodemodemodemodemodemo"
  @State advertise: string = "发现新优惠"

  build() {
    Row() {
      Image(this.avatar)
        .width('12%')
        .borderRadius($r('sys.float.corner_radius_level8'))

      Column() {
        Row() {
          Text(this.title)
            .fontSize($r('app.integer.subtitle_text_S'))
            .fontColor($r('app.color.font_primary'))
            .fontWeight(FontWeight.Medium)
            .padding({ right: 10 })
          Text(this.time)
            .margin({ top: 2 })
            .maxLines(1)
            .width('35%')
            .fontSize($r('app.integer.caption_text_M'))
            .fontColor($r('app.color.font_tertiary'))
            .fontWeight(FontWeight.Regular)
            .textAlign(TextAlign.End)
        }
        .padding({ bottom: 6 })
        .alignItems(VerticalAlign.Top)
        .justifyContent(FlexAlign.SpaceBetween)
        .width('100%')


        Text(this.content)
          .width('80%')
          .maxLines(1)
          .textOverflow({ overflow: TextOverflow.Ellipsis })
          .fontSize($r('app.integer.caption_text_M'))
          .fontColor($r('app.color.font_secondary'))
          .fontWeight(FontWeight.Regular)
      }
      .justifyContent(FlexAlign.Start)
      .alignItems(HorizontalAlign.Start)
      .padding({ left: 12, right: 12 })
      .width('85%')
    }
    .width(CommonConstants.FULL_PERCENT)
    .backgroundColor($r('app.color.comp_background_primary_trans'))
    .padding(12)
    .justifyContent(FlexAlign.SpaceBetween)
    .alignItems(VerticalAlign.Center)
  }
}