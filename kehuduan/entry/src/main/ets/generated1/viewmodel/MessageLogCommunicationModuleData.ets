import LazyDataSource from '../util/LazyDataSource';

export class List_HorizontalListMessageItemModel {
  private static instance: List_HorizontalListMessageItemModel;
  lazyDataSource: LazyDataSource<HorizontalListMessageItemModel> = new LazyDataSource();
  static readonly TITLES: string[] = ['用户A', '用户B', '服务器'];
  static readonly AVATARS: Resource[] = [$r('app.media.user_photo'), $r('app.media.user_photo')];
  static readonly TIMES: string[] = ['10:30:25', '10:31:40', '10:32:15'];
  static readonly CONTENTS: string[] = ['设置信息发送成功', '服务器确认接收', '通信连接正常'];
  static readonly ADVERTISES: string[] = ['高效通信，实时同步', '稳定连接，数据无忧'];

  constructor() {
  }

  public static getInstance(): List_HorizontalListMessageItemModel {
    if (!List_HorizontalListMessageItemModel.instance) {
      List_HorizontalListMessageItemModel.instance =
        new List_HorizontalListMessageItemModel();
    }
    return List_HorizontalListMessageItemModel.instance;
  }

  /**
   * Data loaded on current view converts network data into rendering data
   */
  getResources(): Promise<void> {

    /**
     * use your web request here
     */
    return new Promise((resolve: Function) => {
      const modelList: Array<HorizontalListMessageItemModel> = [];
      for (let index = 0; index < List_HorizontalListMessageItemModel.TITLES.length;
        index++) {
        modelList.push(new HorizontalListMessageItemModel(
          List_HorizontalListMessageItemModel.TITLES[index],
          List_HorizontalListMessageItemModel.AVATARS[index],
          List_HorizontalListMessageItemModel.TIMES[index],
          List_HorizontalListMessageItemModel.CONTENTS[index],
          List_HorizontalListMessageItemModel.ADVERTISES[index],))
      }
      this.lazyDataSource.pushArrayData(modelList);
      resolve();
    });
  }
}

export class HorizontalListMessageItemModel {
  private title: string;
  private avatar: Resource;
  private time: string;
  private content: string;
  private advertise: string;

  constructor(title: string, avatar: Resource, time: string, content: string, advertise: string) {
    this.title = title;
    this.avatar = avatar;
    this.time = time;
    this.content = content;
    this.advertise = advertise;
  }

  getTitle(): string {
    return this.title;
  }

  getAvatar(): Resource {
    return this.avatar;
  }

  getTime(): string {
    return this.time;
  }

  getContent(): string {
    return this.content;
  }

  getAdvertise(): string {
    return this.advertise;
  }
}