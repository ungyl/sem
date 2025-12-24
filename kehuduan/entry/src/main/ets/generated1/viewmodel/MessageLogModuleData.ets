import LazyDataSource from '../util/LazyDataSource';

export class List_HorizontalListMessageItemModel {
  private static instance: List_HorizontalListMessageItemModel;
  lazyDataSource: LazyDataSource<HorizontalListMessageItemModel> = new LazyDataSource();
  static readonly TITLES: string[] =
    ['用户1', '用户2', '用户3', '用户4', '用户5', '用户6', '用户7', '用户8', '用户9', '用户10'];
  static readonly AVATARS: Resource[] =
    [$r('app.media.user_photo'), $r('app.media.user_photo'), $r('app.media.user_photo'), $r('app.media.user_photo'),
      $r('app.media.user_photo'), $r('app.media.user_photo'), $r('app.media.user_photo'), $r('app.media.user_photo'),
      $r('app.media.user_photo'), $r('app.media.user_photo')];
  static readonly TIMES: string[] =
    ['2024-01-15 10:30:25', '2024-01-15 10:28:17', '2024-01-15 10:25:43', '2024-01-15 10:22:59', '2024-01-15 10:20:12',
      '2024-01-15 10:18:34', '2024-01-15 10:15:21', '2024-01-15 10:13:08', '2024-01-15 10:10:55',
      '2024-01-15 10:08:42'];
  static readonly CONTENTS: string[] =
    ['设备温度正常', '数据上传成功', '服务器连接稳定', '指令执行完成', '设备已上线', '数据同步完成', '报警已解除',
      '固件更新成功', '设备重启完成', '配置已保存'];
  static readonly ADVERTISES: string[] =
    ['智能物联，智慧生活', '稳定连接，高效通信', '实时监控，安全可靠', '数据驱动，智能决策', '云端协同，无缝对接',
      '高效传输，低延迟', '全面兼容，易于集成', '智能分析，精准预警', '稳定可靠，值得信赖', '创新科技，引领未来'];

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